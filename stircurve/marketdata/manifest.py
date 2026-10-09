"""Market-data manifest: what is dumped from Bloomberg, how each column is named
and which conventions each instrument follows.

The manifest lives in ``stircurve/config/<ccy>_manifest.yaml``. This module
loads it, checks it against the currency config (every family instrument and
index covered, every calendar a known one) and turns it into the column plan
the dump writes and the loader expects.
"""
from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from ..config.loader import CONFIG_DIR, load_config
from ..refdata.calendars import CALENDAR_NAMES, Calendar

SOURCE_STATUSES = ("captured", "pending_capture", "to_confirm_on_terminal")


def _date(x) -> dt.date | None:
    return None if x in (None, "") else dt.date.fromisoformat(str(x))


@dataclass(frozen=True)
class Series:
    """One Bloomberg ticker (all its fields) as the dump plans it."""
    instrument: str          # manifest key, e.g. 'sofr3m_fut', 'ois_sofr', 'EFFR', 'target_upper'
    contract: str            # futures: '2024-03'; swaps: tenor '2Y'; fixings/anchors: ''
    ticker: str              # canonical ticker (two-digit year for futures)
    fields: tuple[str, ...]
    first_date: dt.date      # first date a value is expected
    last_date: dt.date | None

    def columns(self, fmt: str) -> list[str]:
        return [fmt.format(ticker=self.ticker, field=f) for f in self.fields]


@dataclass
class Manifest:
    currency: str
    raw: dict
    path: Path
    _calendars: dict[str, Calendar] = field(default_factory=dict, repr=False)

    # --- access -------------------------------------------------------------
    @property
    def instruments(self) -> dict[str, dict]:
        return self.raw["instruments"]

    @property
    def fixings(self) -> dict[str, dict]:
        return self.raw["fixings"]

    @property
    def anchors(self) -> dict[str, dict]:
        return self.raw["policy_anchors"]

    @property
    def sources(self) -> dict[str, dict]:
        return self.raw["sources"]

    @property
    def column_format(self) -> str:
        return self.raw["column_format"]

    @property
    def month_codes(self) -> dict[str, int]:
        return self.raw["month_codes"]

    def futures(self) -> dict[str, dict]:
        return {k: v for k, v in self.instruments.items() if v["kind"] == "future"}

    def swaps(self) -> dict[str, dict]:
        return {k: v for k, v in self.instruments.items() if v["kind"] == "swap"}

    def entry(self, name: str) -> dict:
        for group in (self.instruments, self.fixings, self.anchors):
            if name in group:
                return group[name]
        raise KeyError(name)

    def group_of(self, name: str) -> str:
        """CSV file stem for an entry: the instrument key, 'fixings' or 'policy_anchors'."""
        if name in self.instruments:
            return name
        return "fixings" if name in self.fixings else "policy_anchors"

    def calendar(self, name: str) -> Calendar:
        """A committed calendar, or a joint one for 'a+b' (holiday union)."""
        if name not in self._calendars:
            parts = name.split("+")
            if len(parts) == 1:
                self._calendars[name] = Calendar.load(name)
            else:
                hol: dict[dt.date, str] = {}
                for p in parts:
                    hol.update(self.calendar(p).holidays)
                self._calendars[name] = Calendar(name, hol)
        return self._calendars[name]

    # --- tickers --------------------------------------------------------------
    def future_ticker(self, instrument: str, year: int, month: int, two_digit: bool = True) -> str:
        bbg = self.instruments[instrument]["bbg"]
        code = {v: k for k, v in self.month_codes.items()}[month]
        y = f"{year % 100:02d}" if two_digit else f"{year % 10}"
        return f"{bbg['root']}{code}{y} {bbg['yellow_key']}"

    def request_ticker(self, instrument: str, year: int, month: int, last_trade: dt.date, as_of: dt.date) -> str:
        """The form the dump asks Bloomberg for (``bbg.year_digits``): one-digit year
        while the contract trades, two digits once it has expired, and two digits for
        live contracts more than ``live_max_years_ahead`` years out. Bloomberg reads a
        one-digit year as the nearest past decade: on 2026-10-07 'SFRU5' was Sep 2025
        (expired), not Sep 2035 (AC's first dump)."""
        digits = self.instruments[instrument]["bbg"].get("year_digits", {"live": 2, "expired": 2})
        live = last_trade >= as_of
        far = year - as_of.year > digits.get("live_max_years_ahead", 8)
        two = digits["live" if live else "expired"] == 2 or (live and far)
        return self.future_ticker(instrument, year, month, two_digit=two)

    def swap_ticker(self, instrument: str, tenor: str) -> str:
        return self.instruments[instrument]["bbg"]["pattern"].format(code=self.raw["tenor_codes"][tenor])

    def parse_future_ticker(self, ticker: str) -> tuple[str, int, int] | None:
        """'SFRH24 Comdty' -> ('sofr3m_fut', 2024, 3). Two-digit years only (canonical columns)."""
        for name, ins in self.futures().items():
            bbg = ins["bbg"]
            m = re.fullmatch(rf"{re.escape(bbg['root'])}([{''.join(self.month_codes)}])(\d\d) {re.escape(bbg['yellow_key'])}",
                             ticker)
            if m:
                return name, 2000 + int(m.group(2)), self.month_codes[m.group(1)]
        return None

    def contract_fields(self, instrument: str, ref_start: dt.date, end: dt.date) -> tuple[str, ...]:
        """All fields for contracts starting within ``count_fields_months`` of ``end``;
        the quote field (first listed) only beyond that. Far contracts have no open
        interest or volume, and Bloomberg answers those fields with a field exception
        that fails the whole bulk read_bdh call (pdblp raises ValueError)."""
        ins = self.instruments[instrument]
        months = ins.get("count_fields_months")
        if months is None:
            return tuple(ins["fields"])
        y, mo = divmod(end.month - 1 + months, 12)
        horizon = dt.date(end.year + y, mo + 1, 1)
        return tuple(ins["fields"]) if ref_start < horizon else tuple(ins["fields"][:1])

    # --- column plan ------------------------------------------------------------
    def series(self, start: dt.date, end: dt.date) -> list[Series]:
        """Every ticker expected to have a value somewhere in [start, end]."""
        from .contracts import contract_table   # local: contracts imports this module

        out: list[Series] = []
        table = contract_table(self, start, end, listing="dump_listing")   # lean to requesting too much
        for row in table.itertuples():
            ins = self.instruments[row.instrument]
            out.append(Series(row.instrument, row.contract, row.bbg_ticker,
                              self.contract_fields(row.instrument, row.ref_start, end), row.first_quote, row.last_quote))
        for name, ins in self.swaps().items():
            first, last = _date(ins["first_date"]), _date(ins.get("last_date"))
            if _overlaps(first, last, start, end):
                out += [Series(name, t, self.swap_ticker(name, t), tuple(ins["fields"]), first, last)
                        for t in ins["tenors"]]
        for group in (self.fixings, self.anchors):
            for name, e in group.items():
                first, last = _date(e["first_date"]), _date(e.get("last_date"))
                if _overlaps(first, last, start, end):
                    out.append(Series(name, "", e["ticker"], tuple(e["fields"]), first, last))
        return out


def _overlaps(first: dt.date, last: dt.date | None, start: dt.date, end: dt.date) -> bool:
    return first <= end and (last is None or last >= start)


def load_manifest(ccy: str = "usd", path: Path | None = None) -> Manifest:
    p = path or CONFIG_DIR / f"{ccy.lower()}_manifest.yaml"
    with p.open(encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    return Manifest(raw["currency"], raw, p)


# ---------------------------------------------------------------------------
# validation
# ---------------------------------------------------------------------------
def _walk_rules(node, path=""):
    """Yield (path, dict) for every mapping in the manifest that names a source."""
    if isinstance(node, dict):
        if "source" in node:
            yield path, node
        for k, v in node.items():
            yield from _walk_rules(v, f"{path}.{k}" if path else str(k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _walk_rules(v, f"{path}[{i}]")


def _calendar_names(node):
    """Every calendar name the manifest refers to."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ("calendar", "fixing_calendar", "exchange_calendar") and isinstance(v, str) and v != "exchange":
                yield v
            elif k == "calendars" and isinstance(v, list):
                yield from v
            else:
                yield from _calendar_names(v)
    elif isinstance(node, list):
        for v in node:
            yield from _calendar_names(v)


def validate_manifest(m: Manifest) -> list[str]:
    """Problems with the manifest itself and against ``<ccy>.yaml``; empty when complete."""
    problems: list[str] = []
    cfg = load_config(m.raw.get("config", m.currency.lower()))
    for fam, spec in cfg["families"].items():
        for ins in spec["instruments"]:
            if ins not in m.instruments:
                problems.append(f"family {fam}: instrument {ins} missing from manifest")
            elif m.instruments[ins].get("family") != fam:
                problems.append(f"{ins}: family {m.instruments[ins].get('family')!r} != usd.yaml {fam!r}")
        if spec["index"] not in m.fixings:
            problems.append(f"family {fam}: index {spec['index']} has no fixing entry")
    used = {i for spec in cfg["families"].values() for i in spec["instruments"]}
    for ins in set(m.instruments) - used:
        problems.append(f"{ins}: in manifest but in no usd.yaml family")
    for name, ins in m.instruments.items():
        if ins["index"] not in m.fixings:
            problems.append(f"{name}: index {ins['index']} has no fixing entry")
        for key in ("bbg", "fields", "quote", "first_date", "valid_range"):
            if key not in ins:
                problems.append(f"{name}: missing {key}")
        if ins["kind"] == "future":
            for key in ("reference_window", "accrual", "daycount", "exchange_calendar", "last_trade",
                        "final_settlement", "listing", "cycle"):
                if key not in ins:
                    problems.append(f"{name}: missing {key}")
        if ins["kind"] == "swap":
            for t in ins["tenors"]:
                if t not in m.raw["tenor_codes"]:
                    problems.append(f"{name}: tenor {t} has no Bloomberg code")
        if ins.get("quote", {}).get("mid") is not True:
            problems.append(f"{name}: quotes must be mids (D10)")
    for name, a in m.anchors.items():
        for key in ("refdata_anchor", "ticker", "fields", "first_date", "valid_range"):
            if key not in a:
                problems.append(f"policy anchor {name}: missing {key}")
    known = set(CALENDAR_NAMES)
    for cal in set(_calendar_names(m.raw)):
        for part in cal.split("+"):
            if part not in known:
                problems.append(f"unknown calendar {part!r}")
    for path, node in _walk_rules(m.raw):
        src = node["source"]
        if src not in m.sources:
            problems.append(f"{path}: unknown source {src!r}")
    for sid, s in m.sources.items():
        status = s.get("status", "captured")
        if status not in SOURCE_STATUSES:
            problems.append(f"source {sid}: bad status {status!r}")
        if status == "captured" and not s.get("fixture"):
            problems.append(f"source {sid}: captured source needs a fixture name")
    return problems


def normalise(text: str) -> str:
    """Lower-case letters and digits only: PDF text extraction splits words and
    turns quotes into typographic ones, so quotes are matched on this form."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def quotes(m: Manifest) -> list[tuple[str, str, str]]:
    """(rule path, source id, quote) for every rule that cites a passage."""
    out = []
    for path, node in _walk_rules(m.raw):
        if isinstance(node.get("quote"), str):     # (an instrument's ``quote`` mapping is its quote convention)
            out.append((path, node["source"], node["quote"]))
    return out
