"""Bloomberg dump: manifest -> pxts.read_bdh -> wide CSVs under data/market/<ccy>/<YYYY>/.

Runs on a terminal machine; Bloomberg (via pxts/pdblp on localhost:8194) is the
only network it touches. One file per year and group (a futures/swap
instrument, ``fixings`` or ``policy_anchors``), one column per
``<ticker>|<field>`` (canonical tickers: two-digit futures years), ISO dates,
``NaN`` for missing.

Never overwrites silently. The new values are merged into the existing file
and diffed like the reference-data updaters: new dates, new columns and
NaN -> value fills are additions; a changed value or a value that disappears
is blocking (nothing is written, exit 2). Files are written only with
``write_csv=True``; an unchanged file is not rewritten (idempotent).
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from .. import DATA_DIR
from .manifest import Manifest, Series

MARKET_DIR = DATA_DIR / "market"
# seconds pdblp waits for each part of a Bloomberg response (pxts read_bdh ``timeout``).
# It bounds the wait between messages, not the whole request, so a generous value costs
# nothing on calls that succeed: 120 s covers a 50-ticker request over 16 years of daily
# history on a busy terminal.
TIMEOUT = 120
CHUNK = 50          # tickers per read_bdh call
REL_TOL = 1e-12


@dataclass
class FileDiff:
    path: Path
    added_rows: int = 0
    added_columns: list[str] = field(default_factory=list)
    filled: int = 0
    changed: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)

    @property
    def blocking(self) -> bool:
        return bool(self.changed or self.removed)

    @property
    def empty(self) -> bool:
        return not (self.added_rows or self.added_columns or self.filled or self.blocking)

    def report(self) -> str:
        if self.empty:
            return f"{self.path}: no changes"
        lines = [f"{self.path}: +{self.added_rows} rows, +{len(self.added_columns)} columns, {self.filled} NaN->value"]
        for label, items in (("changed", self.changed), ("removed", self.removed)):
            if items:
                lines.append(f"  {label} ({len(items)}):")
                lines += [f"    {x}" for x in items[:50]]
                if len(items) > 50:
                    lines.append(f"    ... {len(items) - 50} more")
        return "\n".join(lines)


class DumpError(RuntimeError):
    """Bloomberg is unusable for this run (no pdblp, no connection, every request failing)."""


@dataclass
class DumpResult:
    diffs: list[FileDiff] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)      # tickers Bloomberg returned nothing for
    reasons: dict[str, int] = field(default_factory=dict)  # error message -> count, for the failed tickers
    empty: list[Path] = field(default_factory=list)       # files with no rows returned (not written)
    written: list[Path] = field(default_factory=list)

    @property
    def blocking(self) -> bool:
        return any(d.blocking for d in self.diffs)

    def report(self) -> str:
        lines = [d.report() for d in self.diffs]
        if self.failed:
            lines.append(f"no data from Bloomberg for {len(self.failed)} ticker-fields (written as NaN; expected for "
                         "contracts not yet listed, since the dump requests generously):")
            lines += [f"  {t}" for t in self.failed[:40]]
            if len(self.failed) > 40:
                lines.append(f"  ... {len(self.failed) - 40} more")
            lines.append("errors behind them:")
            lines += [f"  {n} x {msg}" for msg, n in sorted(self.reasons.items(), key=lambda kv: -kv[1])[:5]]
        for p in self.empty:
            lines.append(f"{p}: Bloomberg returned no rows for the range; not written")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# planning
# ---------------------------------------------------------------------------
def year_ranges(start: dt.date, end: dt.date):
    for y in range(start.year, end.year + 1):
        yield y, max(start, dt.date(y, 1, 1)), min(end, dt.date(y, 12, 31))


def plan(m: Manifest, start: dt.date, end: dt.date, groups: list[str] | None = None
         ) -> dict[tuple[int, str], tuple[dt.date, dt.date, list[Series]]]:
    """{(year, group): (start, end, series)} for every file the dump writes."""
    out = {}
    for y, a, b in year_ranges(start, end):
        for s in m.series(a, b):
            g = m.group_of(s.instrument)
            if groups and g not in groups and s.instrument not in groups:
                continue
            out.setdefault((y, g), (a, b, []))[2].append(s)
    return out


def request_ticker(m: Manifest, s: Series, as_of: dt.date) -> str:
    if m.group_of(s.instrument) in m.futures():
        p = m.parse_future_ticker(s.ticker)
        return m.request_ticker(s.instrument, p[1], p[2], s.last_date, as_of)
    return s.ticker


# ---------------------------------------------------------------------------
# fetching
# ---------------------------------------------------------------------------
def fetch(m: Manifest, series: list[Series], start: dt.date, end: dt.date, as_of: dt.date, read_bdh,
          timeout: float = TIMEOUT, chunk: int = CHUNK, reasons: dict[str, int] | None = None
          ) -> tuple[pd.DataFrame, list[str]]:
    """One wide frame (index: dates, columns: canonical ``ticker|field``) and the
    columns Bloomberg returned nothing for. pxts raises when any ticker in a call
    has no data (the dump requests generously, so this is common): a failing
    chunk is split in halves until the dead tickers are isolated. A timeout is not
    'no data': the call is retried once, then the run stops (``DumpError``) rather
    than bisecting into hundreds of further timeouts."""
    fmt = m.column_format
    by_field: dict[str, dict[str, str]] = {}
    for s in series:
        for f in s.fields:
            by_field.setdefault(f, {})[fmt.format(ticker=s.ticker, field=f)] = request_ticker(m, s, as_of)
    frames, failed = [], []

    def call(req: dict[str, str], f: str) -> pd.DataFrame:
        df = read_bdh(req, start=start.isoformat(), field=f, end=end.isoformat(), timeout=timeout)
        return df.reindex(columns=list(req))

    reasons = {} if reasons is None else reasons

    def bisect(items: list[tuple[str, str]], f: str) -> None:
        try:
            frames.append(call(dict(items), f))
        except Exception as exc:
            if is_timeout(exc):
                try:
                    frames.append(call(dict(items), f))
                    return
                except Exception as again:
                    raise DumpError(f"Bloomberg timed out twice ({len(items)} tickers, {f}, {start}..{end}, "
                                    f"timeout {timeout:g}s): {type(again).__name__}: {again}. "
                                    "Re-run with a larger --timeout or a shorter range / one --group at a time.") from again
            if len(items) == 1:
                failed.append(f"{items[0][0]} (requested {items[0][1]})")
                msg = f"{type(exc).__name__}: {exc}"[:160]
                reasons[msg] = reasons.get(msg, 0) + 1
                return
            half = len(items) // 2
            bisect(items[:half], f)
            bisect(items[half:], f)

    for f, cols in by_field.items():
        items = list(cols.items())
        for i in range(0, len(items), chunk):
            bisect(items[i:i + chunk], f)
    wide = pd.concat(frames, axis=1) if frames else pd.DataFrame()
    wide.index = pd.DatetimeIndex(wide.index).normalize() if len(wide) else pd.DatetimeIndex([])
    wide = wide.loc[(wide.index >= pd.Timestamp(start)) & (wide.index <= pd.Timestamp(end))]
    all_cols = [c for cols in by_field.values() for c in cols]
    wide = wide.reindex(columns=all_cols).astype(float)
    failed += [c for c in all_cols if c in wide and wide[c].isna().all() and not any(c in x for x in failed)]
    return wide.sort_index(), failed


# ---------------------------------------------------------------------------
# merge + diff + write
# ---------------------------------------------------------------------------
def read_wide(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype={"date": str})
    df.index = pd.DatetimeIndex(pd.to_datetime(df.pop("date"), format="%Y-%m-%d"), name="date")
    return df.astype(float)


def write_wide(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    out = df.copy()
    out.index = out.index.strftime("%Y-%m-%d")
    out.index.name = "date"
    out.to_csv(path, na_rep="NaN", lineterminator="\n")


def merge(existing: pd.DataFrame | None, new: pd.DataFrame, path: Path) -> tuple[pd.DataFrame, FileDiff]:
    diff = FileDiff(path)
    if existing is None:
        diff.added_rows, diff.added_columns = len(new), list(new.columns)
        return new, diff
    cols = list(existing.columns) + [c for c in new.columns if c not in existing.columns]
    idx = existing.index.union(new.index)
    diff.added_rows = len(idx) - len(existing.index)
    diff.added_columns = [c for c in new.columns if c not in existing.columns]
    old = existing.reindex(index=idx, columns=cols)
    upd = new.reindex(index=idx, columns=cols)
    in_new = pd.DataFrame(np.outer(idx.isin(new.index), pd.Index(cols).isin(new.columns)), index=idx, columns=cols)
    in_old = pd.DataFrame(np.outer(idx.isin(existing.index), pd.Index(cols).isin(existing.columns)), index=idx, columns=cols)
    close = np.isclose(old.fillna(0).to_numpy(), upd.fillna(0).to_numpy(), rtol=REL_TOL, atol=0.0)
    changed = old.notna() & upd.notna() & ~close
    removed = old.notna() & upd.isna() & in_new          # fetched again, Bloomberg no longer has it
    diff.filled = int((old.isna() & upd.notna() & in_old).to_numpy().sum())
    for mask, out, fmt in ((changed, diff.changed, "{d} {c}: {o!r} -> {n!r}"), (removed, diff.removed, "{d} {c}: {o!r} -> NaN")):
        for i, j in np.argwhere(mask.to_numpy()):
            d, c = idx[i], cols[j]
            out.append(fmt.format(d=f"{d:%Y-%m-%d}", c=c, o=old.iat[i, j], n=upd.iat[i, j]))
    return old.where(old.notna(), upd).sort_index(), diff


def market_path(root: Path, ccy: str, year: int, group: str) -> Path:
    return root / ccy.lower() / f"{year}" / f"{group}.csv"


def is_timeout(exc: Exception) -> bool:
    """pdblp raises RuntimeError('Timeout ...') when no response arrives in time."""
    return isinstance(exc, TimeoutError) or "timeout" in str(exc).lower() or "timed out" in str(exc).lower()


def probe(m: Manifest, read_bdh, start: dt.date, end: dt.date, timeout: float) -> None:
    """One request for a ticker that always has data (EFFR) before the real run, so a
    missing pdblp or a refused connection stops the run with its own error instead of
    turning into hundreds of 'no data' columns."""
    ticker = m.fixings["EFFR"]["ticker"]
    try:
        df = read_bdh({"probe": ticker}, start=(start - dt.timedelta(days=14)).isoformat(), field="PX_LAST",
                      end=end.isoformat(), timeout=timeout)
    except TypeError as exc:
        if "timeout" in str(exc):
            raise DumpError("pxts.read_bdh has no 'timeout' argument: upgrade pxts "
                            "(pip install -U \"pxts[bloomberg] @ git+https://github.com/adrianchiu1/pxts\")") from exc
        raise DumpError(f"Bloomberg probe ({ticker} PX_LAST) failed: {type(exc).__name__}: {exc}") from exc
    except Exception as exc:
        hint = (" Is the terminal logged in, with the API on localhost:8194? Try a larger --timeout."
                if is_timeout(exc) else "")
        raise DumpError(f"Bloomberg probe ({ticker} PX_LAST) failed: {type(exc).__name__}: {exc}.{hint}") from exc
    if df is None or len(df) == 0:
        raise DumpError(f"Bloomberg probe ({ticker} PX_LAST) returned no rows for {start - dt.timedelta(days=14)}..{end}")


def dump(m: Manifest, start: dt.date, end: dt.date, read_bdh=None, *, write_csv: bool = False,
         as_of: dt.date | None = None, root: Path = MARKET_DIR, groups: list[str] | None = None,
         timeout: float = TIMEOUT, chunk: int = CHUNK) -> DumpResult:
    if read_bdh is None:
        from pxts import read_bdh   # terminal machines only (pip install -e .[bloomberg])
    as_of = as_of or dt.date.today()
    probe(m, read_bdh, start, end, timeout)
    result = DumpResult()
    staged, requested = [], 0
    for (year, group), (a, b, series) in sorted(plan(m, start, end, groups).items()):
        new, failed = fetch(m, series, a, b, as_of, read_bdh, timeout=timeout, chunk=chunk, reasons=result.reasons)
        result.failed += failed
        requested += sum(len(s.fields) for s in series)
        path = market_path(root, m.currency, year, group)
        if new.empty:
            result.empty.append(path)
            continue
        existing = read_wide(path) if path.exists() else None
        merged, diff = merge(existing, new, path)
        result.diffs.append(diff)
        if not diff.empty:
            staged.append((merged, path))
    if requested and len(result.failed) == requested:
        top = max(result.reasons, key=result.reasons.get) if result.reasons else "unknown"
        raise DumpError(f"Bloomberg returned nothing for any of {requested} ticker-fields; nothing written. "
                        f"Most common error: {top}")
    if write_csv and not result.blocking:
        for merged, path in staged:
            write_wide(merged, path)
            result.written.append(path)
    return result
