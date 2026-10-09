"""Load the wide Bloomberg CSVs into a tidy frame and validate them against the manifest.

``load(m, start, end)`` returns ``(frame, report)``: the frame has one row per
(date, instrument, contract, field) with ``value``; contract is 'YYYY-MM' for
futures, the tenor for swaps and '' for fixings and anchors. Values outside an
instrument's window (before listing, after last trade/conversion, outside
first/last dates) are reported and left out of the frame.

Checks (``Report``):
  blocking  unknown columns (no manifest entry, wrong file, unknown field, unlisted
            contract), malformed files (bad dates, duplicate dates, non-numbers),
            out-of-range values, futures quoted after their last quote date or
            before a verified listing date
  warnings  missing expected columns, stale values (unchanged ``stale_days`` or
            more), quotes before an unsourced listing date (kept in the frame: the
            data shows the real listing), fixings/swaps outside
            their first/last dates
Exit code 2 when anything is blocking (as the updaters), else 0.
"""
from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from .contracts import contract_table, listed_contracts
from .dump import MARKET_DIR
from .manifest import Manifest, _date

QUOTE_FIELDS = ("PX_LAST", "PX_SETTLE", "PX_MID")
COUNT_FIELDS = ("OPEN_INT", "PX_VOLUME")
CHECKS = ("unknown_columns", "malformed", "out_of_range", "outside_listing", "missing_columns",
          "stale", "outside_listing_unverified", "outside_dates")
BLOCKING = ("unknown_columns", "malformed", "out_of_range", "outside_listing")


@dataclass
class Report:
    files: list[str] = field(default_factory=list)
    columns: int = 0
    values: int = 0
    found: dict[str, list[str]] = field(default_factory=lambda: {k: [] for k in CHECKS})

    def add(self, check: str, msg: str) -> None:
        self.found[check].append(msg)

    @property
    def blocking(self) -> bool:
        return any(self.found[k] for k in BLOCKING)

    @property
    def exit_code(self) -> int:
        return 2 if self.blocking else 0

    def summary(self) -> dict[str, int]:
        return {k: len(v) for k, v in self.found.items()}

    def report(self, limit: int = 40) -> str:
        lines = [f"{len(self.files)} file(s), {self.columns} columns, {self.values} values"]
        for k in CHECKS:
            items = self.found[k]
            tag = "BLOCKING" if k in BLOCKING else "warning"
            lines.append(f"{k}: {len(items)}" + (f" ({tag})" if items else ""))
            lines += [f"  {x}" for x in items[:limit]]
            if len(items) > limit:
                lines.append(f"  ... {len(items) - limit} more")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# column mapping
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ColumnInfo:
    instrument: str
    contract: str
    field: str


def column_map(m: Manifest, group: str, columns: list[str], contracts: dict[tuple[str, str], object]
               ) -> tuple[dict[str, ColumnInfo], list[str]]:
    """Map each column of a ``group`` file to a manifest entry; return (mapped, unknown messages)."""
    swap_tickers = {m.swap_ticker(n, t): (n, t) for n, ins in m.swaps().items() for t in ins["tenors"]}
    plain = {e["ticker"]: n for grp in (m.fixings, m.anchors) for n, e in grp.items()}
    mapped, unknown = {}, []
    for col in columns:
        ticker, sep, fld = col.rpartition("|")
        if not sep:
            unknown.append(f"{group}: {col!r}: not '<ticker>|<field>'")
            continue
        fut = m.parse_future_ticker(ticker)
        if fut:
            name, contract = fut[0], f"{fut[1]}-{fut[2]:02d}"
            if (name, contract) not in contracts:
                unknown.append(f"{group}: {col}: {name} {contract} is not a listed contract in range")
                continue
        elif ticker in swap_tickers:
            name, contract = swap_tickers[ticker]
        elif ticker in plain:
            name, contract = plain[ticker], ""
        else:
            unknown.append(f"{group}: {col}: ticker not in the manifest")
            continue
        if m.group_of(name) != group:
            unknown.append(f"{group}: {col}: belongs in {m.group_of(name)}.csv")
            continue
        if fld not in m.entry(name)["fields"]:
            unknown.append(f"{group}: {col}: field {fld} not in the manifest for {name}")
            continue
        mapped[col] = ColumnInfo(name, contract, fld)
    return mapped, unknown


# ---------------------------------------------------------------------------
# reading
# ---------------------------------------------------------------------------
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _read(path: Path, report: Report) -> pd.DataFrame | None:
    raw = pd.read_csv(path, dtype=str, keep_default_na=False)
    if raw.columns[0] != "date":
        report.add("malformed", f"{path}: first column is {raw.columns[0]!r}, not 'date'")
        return None
    bad = [d for d in raw["date"] if not DATE_RE.fullmatch(d)]
    if bad:
        report.add("malformed", f"{path}: non-ISO dates {bad[:3]}")
        return None
    if raw["date"].duplicated().any():
        report.add("malformed", f"{path}: duplicate dates {sorted(set(raw['date'][raw['date'].duplicated()]))[:3]}")
        return None
    if list(raw.columns).count("date") > 1 or raw.columns.duplicated().any():
        report.add("malformed", f"{path}: duplicate columns")
        return None
    df = raw.set_index("date")
    num = df.apply(lambda s: pd.to_numeric(s.replace({"": "NaN"}), errors="coerce"))
    nonnum = (num.isna() & ~df.isin(["", "NaN", "nan"]))
    if nonnum.to_numpy().any():
        r, c = np.argwhere(nonnum.to_numpy())[0]
        report.add("malformed", f"{path}: non-numeric value {df.iat[r, c]!r} at {df.index[r]} {df.columns[c]}")
        return None
    num.index = pd.DatetimeIndex(pd.to_datetime(num.index, format="%Y-%m-%d"), name="date")
    return num.sort_index()


def market_files(m: Manifest, root: Path, start: dt.date | None, end: dt.date | None) -> list[tuple[int, str, Path]]:
    base = root / m.currency.lower()
    out = []
    for p in sorted(base.glob("[0-9][0-9][0-9][0-9]/*.csv")):
        y = int(p.parent.name)
        if (start and y < start.year) or (end and y > end.year):
            continue
        out.append((y, p.stem, p))
    return out


# ---------------------------------------------------------------------------
# validation
# ---------------------------------------------------------------------------
def _stale_runs(s: pd.Series, n: int) -> list[tuple[pd.Timestamp, pd.Timestamp, int]]:
    v = s.dropna()
    if len(v) < n:
        return []
    run_id = (v != v.shift()).cumsum()
    out = []
    for _, grp in v.groupby(run_id):
        if len(grp) >= n:
            out.append((grp.index[0], grp.index[-1], len(grp)))
    return out


def load(m: Manifest, start: dt.date | None = None, end: dt.date | None = None,
         root: Path = MARKET_DIR) -> tuple[pd.DataFrame, Report]:
    report = Report()
    frames = []
    for year, group, path in market_files(m, root, start, end):
        report.files.append(str(path))
        if group not in m.instruments and group not in ("fixings", "policy_anchors"):
            report.add("unknown_columns", f"{path}: file {group}.csv matches no manifest group")
            continue
        wide = _read(path, report)
        if wide is None:
            continue
        if start or end:
            wide = wide.loc[(wide.index >= pd.Timestamp(start or dt.date.min)) &
                            (wide.index <= pd.Timestamp(end or dt.date.max))]
        if wide.empty:
            continue
        d0, d1 = wide.index[0].date(), wide.index[-1].date()
        # columns map against what the dump requests (generous horizon); listing dates come
        # from the exchange schedule (a contract not yet listed there by d1 has none)
        ctab = contract_table(m, d0, d1, [group], listing="dump_listing") if group in m.futures() else None
        contracts = {(r.instrument, r.contract): r for r in ctab.itertuples()} if ctab is not None else {}
        exchange = ({c.contract: c for c in listed_contracts(m, group, d1)} if ctab is not None else {})
        mapped, unknown = column_map(m, group, list(wide.columns), contracts)
        for u in unknown:
            report.add("unknown_columns", u)
        report.columns += len(wide.columns)

        expected = {c for s in m.series(d0, d1) if m.group_of(s.instrument) == group
                    for c in s.columns(m.column_format)}
        for c in sorted(expected - set(wide.columns)):
            report.add("missing_columns", f"{path}: {c}")

        for col, info in mapped.items():
            s = wide[col]
            e = m.entry(info.instrument)
            keep = s.notna()
            report.values += int(keep.sum())
            # range
            lo, hi = (e["valid_range"] if info.field not in COUNT_FIELDS else (0, np.inf))
            bad = s[(s < lo) | (s > hi)]
            for d, v in bad.items():
                report.add("out_of_range", f"{path}: {d:%Y-%m-%d} {col} = {v} outside [{lo}, {hi}]")
            # window
            if ctab is not None:
                c = contracts[(info.instrument, info.contract)]
                late = s.notna() & (s.index > pd.Timestamp(c.last_quote))
                x = exchange.get(info.contract)       # None: not listed by d1 under the exchange schedule
                listed = pd.Timestamp(x.first_listed) if x else pd.Timestamp.max
                verified = bool(x and x.listing_verified)
                early = s.notna() & (s.index < listed)
                for d in s.index[late]:
                    report.add("outside_listing", f"{path}: {d:%Y-%m-%d} {col} after last quote date {c.last_quote}")
                if early.any():
                    when = x.first_listed if x else f"after {d1}"
                    if verified:
                        for d in s.index[early]:
                            report.add("outside_listing", f"{path}: {d:%Y-%m-%d} {col} before first listed {when}")
                        keep &= ~early
                    else:   # schedule unsourced: the data shows the real listing; keep the values
                        report.add("outside_listing_unverified",
                                   f"{path}: {col} quoted from {s.index[early][0]:%Y-%m-%d}, modelled first listing {when}")
                keep &= ~late
            first, last = _date(e["first_date"]), _date(e.get("last_date"))
            outside = s.notna() & ((s.index < pd.Timestamp(first)) |
                                   (s.index > pd.Timestamp(last or dt.date.max)))
            if outside.any() and ctab is None:
                report.add("outside_dates", f"{path}: {col} has {int(outside.sum())} values outside "
                                            f"[{first}, {last or 'open'}], e.g. {s.index[outside][0]:%Y-%m-%d}")
            keep &= ~outside
            # staleness (quote fields only)
            n = e.get("stale_days")
            if n and info.field in QUOTE_FIELDS:
                for a, b, k in _stale_runs(s[keep], n):
                    report.add("stale", f"{path}: {col} unchanged {k} days {a:%Y-%m-%d}..{b:%Y-%m-%d}")
            v = s[keep]
            frames.append(pd.DataFrame({"date": v.index, "instrument": info.instrument, "contract": info.contract,
                                        "field": info.field, "value": v.to_numpy()}))
    cols = ["date", "instrument", "contract", "field", "value"]
    frame = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=cols)
    frame = frame.sort_values(cols[:4], ignore_index=True)
    return frame, report
