"""Reference-data updater.

Behaviour (spec, "Reference data"): parse → validate → diff against the
committed file → print the diff → exit non-zero on any removed row or any
changed *past* date. New rows are written only with ``commit=True``.
Synthetic rows are never written by the updater (they are generated at
build time), and a published row always replaces a synthetic one.
"""
from __future__ import annotations

import datetime as dt
import functools
import math
import re
from dataclasses import dataclass, field
from pathlib import Path

from .. import REFDATA_DIR
from .calendars import CALENDAR_NAMES, HOLIDAY_YEARS, SIFMA_UNSCHEDULED_CLOSES, Calendar

# rule dates sourced individually (not in the annual schedules the updater reads)
SOURCED_ONE_OFFS = set(SIFMA_UNSCHEDULED_CLOSES)
from .maintenance import (MaintenancePeriod, PolicyRate, load_maintenance_periods, load_policy_rates, rate_in_effect,
                          save_maintenance_periods, save_policy_rates, validate_maintenance_periods)
from .meetings import (BANK_CALENDAR, Meeting, effective_date, load_meetings, load_published_effective,
                       published_lookup, save_meetings)
from .parsers import banks as bank_parsers
from .parsers import holidays as holiday_parsers
from .parsers import policy_rates as pr_parsers
from .parsers.common import saving_fixtures, today_iso


def _fixture_capture(fn):
    """Add a ``save_fixtures`` keyword: a directory that receives the text of
    every page fetched during the call (``<source>_<YYYYMMDD>.txt``)."""
    @functools.wraps(fn)
    def wrapper(*args, save_fixtures: Path | str | None = None, **kwargs):
        with saving_fixtures(save_fixtures):
            return fn(*args, **kwargs)
    return wrapper


@dataclass
class Diff:
    added: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    changed: list[str] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)

    @property
    def blocking(self) -> bool:
        return bool(self.removed or self.changed or self.problems)

    def report(self) -> str:
        lines = []
        for label, items in (("added", self.added), ("removed", self.removed),
                             ("changed", self.changed), ("problems", self.problems)):
            if items:
                lines.append(f"{label} ({len(items)}):")
                lines += [f"  {x}" for x in items]
        return "\n".join(lines) if lines else "no changes"


# ---------------------------------------------------------------------------
# meetings
# ---------------------------------------------------------------------------
@_fixture_capture
def update_meetings(bank: str, commit: bool = False, historical_years: range | None = None,
                    refdata_dir: Path = REFDATA_DIR, today: dt.date | None = None) -> Diff:
    today = today or dt.date.today()
    cal = Calendar.load(BANK_CALENDAR[bank], refdata_dir=refdata_dir)
    lookup = published_lookup(bank, refdata_dir)
    overrides = load_published_effective(bank, refdata_dir)

    if bank == "fed":
        fetched = bank_parsers.fetch_fed(historical_years)
    elif bank == "boe":
        fetched = bank_parsers.fetch_boe()
    elif bank == "boj":
        # schedule pages (this year, next, 2010+) and the minutes indexes (1998+); the minutes
        # of new or recent one-day meetings are read to find unscheduled ones
        committed = {m.decision_date for m in load_meetings(bank, True, refdata_dir)}
        recent = today - dt.timedelta(days=400)
        fetched = bank_parsers.fetch_boj()
        fetched += bank_parsers.fetch_boj_minutes(   # --historical: re-read every one-day meeting in range
            historical_years, classify=None if historical_years else (lambda d: d not in committed or d >= recent))
    elif bank == "ecb":
        # ECB meetings come from the maintenance-period tables (relevant GC meeting column)
        # (an open last MP, end "tbd", still publishes its meeting and start date)
        rows = [(row, url) for row, url in bank_parsers.fetch_ecb_maintenance(historical_years, include_open=True)
                if row.get("meeting")]
        fetched = [(row["meeting"], "scheduled", url) for row, url in rows]
        lookup.update({row["meeting"]: row["start"] for row, _ in rows if row["end"] is None})
    else:
        raise ValueError(bank)

    if bank in ("fed", "boj"):   # match rate changes to the fetched decisions too, not only committed ones
        lookup.update(published_lookup(bank, refdata_dir, decisions=[d for d, k, _ in fetched if k != "skip"]
                                       + [m.decision_date for m in load_meetings(bank, True, refdata_dir)]))
        lookup.update({d: e for d, (e, _) in overrides.items()})

    new: dict[dt.date, Meeting] = {}
    for d, kind, url in fetched:
        if kind == "skip" or (d in new and not new[d].scheduled):
            continue    # a source that marks the decision unscheduled wins over a schedule table
        new[d] = Meeting(bank, d, effective_date(bank, d, cal, lookup), scheduled=(kind == "scheduled"),
                         regime=_regime(bank, d), synthetic=False, source_url=url, retrieved_at=today_iso())

    # a decision already filed as unscheduled stays there (the BoE workbook and the
    # BoJ tables do not mark special meetings; boe_unscheduled.csv does, with sources)
    for d in {m.decision_date for m in _load_unscheduled(bank, refdata_dir)} & set(new):
        new[d] = Meeting(bank, d, new[d].effective_date, scheduled=False, regime=new[d].regime,
                         source_url=new[d].source_url, retrieved_at=new[d].retrieved_at)

    diff = Diff()
    merged_by_kind: dict[bool, dict[dt.date, Meeting]] = {}
    for unsched in (False, True):
        existing = {m.decision_date: m for m in load_meetings(bank, False, refdata_dir)
                    if m.scheduled != unsched}
        if unsched:
            existing = {m.decision_date: m for m in _load_unscheduled(bank, refdata_dir)}
        incoming = {d: m for d, m in new.items() if m.scheduled != unsched}
        merged = dict(existing)
        for d, m in incoming.items():
            if d not in existing:
                diff.added.append(f"{bank} {'unscheduled' if unsched else 'scheduled'} {d} eff {m.effective_date} ({m.source_url})")
                merged[d] = m
            elif existing[d].effective_date != m.effective_date:
                msg = f"{bank} {d}: effective {existing[d].effective_date} -> {m.effective_date}"
                if d in overrides and overrides[d][0] == m.effective_date:
                    # from the reviewed published_effective.csv, not from a scraped page
                    diff.added.append(f"{msg} (published: {overrides[d][1]})")
                    merged[d] = m
                elif lookup.get(d) == m.effective_date and bank in ("fed", "boj", "ecb"):
                    # from committed published data: rate-change dates (D16) or the MP table
                    diff.added.append(f"{msg} (published implementation date)")
                    merged[d] = m
                else:
                    (diff.changed if d <= today else diff.added).append(msg)
                    if d > today:
                        merged[d] = m
        # rows the source no longer shows: only a problem if the source covered that period
        covered_years = {d.year for d in incoming}
        for d in existing:
            if d.year in covered_years and d not in incoming and d > today:
                diff.removed.append(f"{bank} {d} no longer on source page")
        merged_by_kind[unsched] = merged
    # a decision filed (with its source) as unscheduled leaves the scheduled file
    for d in sorted(set(merged_by_kind[False]) & set(merged_by_kind[True])):
        diff.added.append(f"{bank} {d}: moved to {bank}_unscheduled.csv ({merged_by_kind[True][d].source_url})")
        del merged_by_kind[False][d]
    diff.problems += _near_duplicates(bank, [m for ms in merged_by_kind.values() for m in ms.values()])
    if commit and not diff.blocking:
        for unsched, merged in merged_by_kind.items():
            save_meetings(bank, list(merged.values()), unscheduled=unsched, refdata_dir=refdata_dir)
    return diff


def _near_duplicates(bank: str, meetings: list[Meeting], days: int = 4) -> list[str]:
    """Two decisions a few days apart from *different* sources are almost always
    one meeting dated two ways (meeting day vs announcement day): a question,
    not an add. Entries on one source page are distinct events (FOMC calls of
    13 and 17 Sep 2001), as is an unscheduled meeting right after a scheduled
    one (BoJ 17 and 18 Sep 2008)."""
    ms = sorted(meetings, key=lambda m: m.decision_date)
    return [f"{bank} {a.decision_date} and {b.decision_date} are {(b.decision_date - a.decision_date).days} days apart "
            f"({a.source_url} / {b.source_url}): same decision?"
            for a, b in zip(ms, ms[1:])
            if (b.decision_date - a.decision_date).days <= days and a.source_url != b.source_url
            and a.scheduled == b.scheduled]


def _load_unscheduled(bank: str, refdata_dir: Path) -> list[Meeting]:
    from .meetings import meetings_path
    import csv
    p = meetings_path(bank, True, refdata_dir)
    if not p.exists():
        return []
    out = []
    with p.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row.get("decision_date"):
                out.append(Meeting(bank, dt.date.fromisoformat(row["decision_date"]),
                                   dt.date.fromisoformat(row["effective_date"]), scheduled=False,
                                   regime=row.get("regime", ""), source_url=row.get("source_url", ""),
                                   retrieved_at=row.get("retrieved_at", "")))
    return out


def _regime(bank: str, d: dt.date) -> str:
    if bank == "ecb":
        if d < dt.date(2004, 3, 10):
            return "ecb_pre2004"
        if d < dt.date(2015, 1, 1):
            return "ecb_monthly"
        return "ecb_sixweekly"
    if bank == "boe":
        return "boe_monthly" if d < dt.date(2016, 9, 1) else "boe_eight"
    if bank == "boj":
        return "boj_fourteen" if d < dt.date(2016, 1, 1) else "boj_eight"
    return "fomc_eight"


# ---------------------------------------------------------------------------
# ECB maintenance periods
# ---------------------------------------------------------------------------
@_fixture_capture
def update_ecb_maintenance(commit: bool = False, years: range | None = None,
                           refdata_dir: Path = REFDATA_DIR, today: dt.date | None = None) -> Diff:
    today = today or dt.date.today()
    fetched = bank_parsers.fetch_ecb_maintenance(years)
    existing = {m.start: m for m in load_maintenance_periods(refdata_dir)}
    diff = Diff()
    merged = dict(existing)
    for row, url in fetched:
        m = MaintenancePeriod(row["label"], row["meeting"], row["start"], row["end"], url, today_iso())
        if m.start not in existing:
            diff.added.append(f"MP {m.label} {m.start}..{m.end} meeting {m.meeting_decision_date}")
            merged[m.start] = m
        else:
            old = existing[m.start]
            if (old.end, old.meeting_decision_date) != (m.end, m.meeting_decision_date):
                msg = f"MP {m.label} {m.start}: {old.end}/{old.meeting_decision_date} -> {m.end}/{m.meeting_decision_date}"
                (diff.changed if m.start <= today else diff.added).append(msg)
                if m.start > today:
                    merged[m.start] = m
    diff.problems += validate_maintenance_periods(sorted(merged.values(), key=lambda x: x.start))
    if commit and not diff.blocking:
        save_maintenance_periods(list(merged.values()), refdata_dir)
    return diff


# ---------------------------------------------------------------------------
# holidays
# ---------------------------------------------------------------------------
@_fixture_capture
def update_holidays(name: str, commit: bool = False, years: range = HOLIDAY_YEARS,
                    refdata_dir: Path = REFDATA_DIR) -> Diff:
    """Write the merged rule+official holiday file for one calendar."""
    if name not in CALENDAR_NAMES:
        raise ValueError(name)
    official: dict[dt.date, str] = {}
    source = "rule"
    covered_range = None      # dates the official source speaks for; default: years it lists 3+ dates in
    undated: set[tuple[int, str]] = set()
    if name == "uk":
        official, source = holiday_parsers.fetch_uk(), holiday_parsers.UK_JSON_URL
    elif name == "jp":
        official, source = holiday_parsers.fetch_jp(), holiday_parsers.JP_CSV_URL
    elif name == "us_sifma":
        (official, undated), source = holiday_parsers.fetch_sifma(), holiday_parsers.SIFMA_URL
    elif name == "us_sofr":
        published = holiday_parsers.fetch_sofr_publication_days()
        official = holiday_parsers.sofr_non_publication_days(published)
        source = holiday_parsers.NYFED_SOFR_URL.format(end=max(published).isoformat())
        covered_range = (min(published), max(published))
    cal = Calendar.from_rules(name, years)
    existing = Calendar.load(name, years, refdata_dir)
    official = {d: n for d, n in official.items() if d.year in years}   # e.g. the CAO CSV starts in 1955
    diff = Diff()
    merged = dict(cal.holidays)
    for d, n in official.items():
        if d not in merged:          # rule names are kept for dates both have (stable, English)
            diff.added.append(f"{name} {d} {n} (official, not in rules)")
            merged[d] = n
    # years the official source covers (several dates, not just next year's 1 January):
    # rule-only dates inside them that the source lacks are suspicious
    per_year: dict[int, int] = {}
    for d in official:
        per_year[d.year] = per_year.get(d.year, 0) + 1
    covered = {y for y, n in per_year.items() if n >= 3}
    for d, n in cal.holidays.items():
        in_cover = covered_range[0] <= d <= covered_range[1] if covered_range else d.year in covered
        if (in_cover and d not in official and n != "Bank Holiday" and not n.endswith("(observed)")
                and d not in SOURCED_ONE_OFFS and d.weekday() < 5
                and (d.year, holiday_parsers.holiday_key(n)) not in undated):
            diff.problems.append(f"{name} {d} {n}: in rules but not in official source")
    # rule-generated rows follow the rules; only a row that came from a source blocks when it disappears
    existing_source = _holiday_sources(refdata_dir / "holidays" / f"{name}.csv")
    for d in existing.holidays:
        if d not in merged:
            msg = f"{name} {d} {existing.holidays[d]}"
            if existing_source.get(d, "rule") == "rule":
                diff.added.append(f"{msg}: dropped by the current rules")
            else:
                diff.removed.append(msg)
    if commit and not diff.blocking:
        out = Calendar(name, merged)
        out.write_csv(refdata_dir / "holidays" / f"{name}.csv",
                      source={d: source for d in official} if official else source)
    return diff


def _holiday_sources(path: Path) -> dict[dt.date, str]:
    import csv
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as fh:
        return {dt.date.fromisoformat(r["date"]): r.get("source", "rule") for r in csv.DictReader(fh)}


def write_rule_holidays(refdata_dir: Path = REFDATA_DIR, years: range = HOLIDAY_YEARS) -> None:
    """Seed all five holiday CSVs from rules (no network). Used at repo bootstrap."""
    (refdata_dir / "holidays").mkdir(parents=True, exist_ok=True)
    for name in CALENDAR_NAMES:
        Calendar.from_rules(name, years).write_csv(refdata_dir / "holidays" / f"{name}.csv", source="rule")


# ---------------------------------------------------------------------------
# policy rates
# ---------------------------------------------------------------------------
@_fixture_capture
def update_policy_rates(bank: str, commit: bool = False, refdata_dir: Path = REFDATA_DIR,
                        today: dt.date | None = None) -> Diff:
    """Fed: target range from the open-market table, IORB/IOER from FRED.
    ECB: key-rates table. BoE: Bank Rate table. BoJ: hand-maintained (no-op).
    A primary-sourced row replaces a memory/derived row with the same anchor and date;
    a primary row that contradicts an existing primary row on a past date is blocking."""
    today = today or dt.date.today()
    fetched: list[PolicyRate] = []
    if bank == "fed":
        for r in pr_parsers.fetch_fed_openmarket():
            d = r["effective_date"]
            fetched += [PolicyRate(d, "target_lower", r["lower"], "primary", pr_parsers.FED_OPENMARKET_URL, today_iso()),
                        PolicyRate(d, "target_upper", r["upper"], "primary", pr_parsers.FED_OPENMARKET_URL, today_iso()),
                        PolicyRate(d, "target_midpoint", round((r["lower"] + r["upper"]) / 2, 4), "derived", pr_parsers.FED_OPENMARKET_URL, today_iso())]
        # single target before the open-market table's coverage (it starts 2003): FRED DFEDTAR (1982-2008)
        first_om = min((r.effective_date for r in fetched), default=dt.date.max)
        try:
            for d, v in pr_parsers.fetch_fred("DFEDTAR"):
                if d < first_om:
                    src = pr_parsers.FRED_CSV_URL.format(series="DFEDTAR")
                    fetched += [PolicyRate(d, "target_lower", v, "primary", src, today_iso()),
                                PolicyRate(d, "target_upper", v, "primary", src, today_iso()),
                                PolicyRate(d, "target_midpoint", v, "derived", src, today_iso())]
        except Exception as exc:  # pragma: no cover
            print(f"  fred DFEDTAR: fetch failed ({exc})")
        for series, anchor in (("IORB", "iorb"), ("IOER", "ioer")):
            try:
                for d, v in pr_parsers.fetch_fred(series):
                    fetched.append(PolicyRate(d, anchor, v, "primary", pr_parsers.FRED_CSV_URL.format(series=series), today_iso()))
            except Exception as exc:  # pragma: no cover
                print(f"  fred {series}: fetch failed ({exc})")
    elif bank == "ecb":
        for r in pr_parsers.fetch_ecb_key_rates():
            for k in ("dfr", "mro", "mlf"):
                if k in r:
                    fetched.append(PolicyRate(r["effective_date"], k, r[k], "primary", pr_parsers.ECB_KEY_RATES_URL, today_iso()))
    elif bank == "boe":
        for d, v in pr_parsers.fetch_boe_bank_rate():
            fetched.append(PolicyRate(d, "bank_rate", v, "primary", pr_parsers.BOE_BANK_RATE_URL, today_iso()))
    elif bank == "boj":
        fetched, problems = _boj_policy_rates(refdata_dir, today)
    else:
        raise ValueError(bank)
    if bank != "boj":
        problems = []

    existing = {(r.anchor, r.effective_date): r for r in load_policy_rates(bank, refdata_dir)}
    diff, merged = Diff(), dict(existing)
    diff.problems += problems
    for r in fetched:
        key = (r.anchor, r.effective_date)
        old = existing.get(key)
        if old is None:
            diff.added.append(f"{bank} {r.anchor} {r.effective_date} = {r.rate}")
            merged[key] = r
        elif abs(old.rate - r.rate) > 1e-9 and not (math.isnan(old.rate) and math.isnan(r.rate)):
            msg = f"{bank} {r.anchor} {r.effective_date}: {old.rate} -> {r.rate} (was {old.confidence})"
            if old.confidence.startswith("primary") and r.effective_date <= today:
                diff.changed.append(msg)
            else:
                diff.added.append(msg)
                merged[key] = r
        elif not old.confidence.startswith("primary") and old.confidence != r.confidence:
            diff.added.append(f"{bank} {r.anchor} {r.effective_date}: confirmed ({old.confidence} -> {r.confidence})")
            merged[key] = r
    if commit and not diff.blocking:
        save_policy_rates(bank, list(merged.values()), refdata_dir)
    return diff


def _boj_policy_rates(refdata_dir: Path, today: dt.date) -> tuple[list[PolicyRate], list[str]]:
    """BoJ: basic loan rate from the BoJ CSVs (full history); call-rate target and
    complementary deposit facility rate from the statements of meetings in the
    last 400 days, added only when the level changes. History before that is
    curated from the statements (one source_url per row). A statement that sets
    a guideline the parser cannot read is a problem: probably a new regime."""
    rows = [PolicyRate(d, "basic_loan_rate", v, "primary", url, today_iso())
            for d, v, url in pr_parsers.fetch_boj_discount()]
    problems: list[str] = []
    committed = load_policy_rates("boj", refdata_dir)
    cal = Calendar.load("jp", refdata_dir=refdata_dir)
    lookup = published_lookup("boj", refdata_dir)
    recent = [m for m in load_meetings("boj", True, refdata_dir)
              if today - dt.timedelta(days=400) <= m.decision_date <= today]
    for m in recent:
        got = pr_parsers.fetch_boj_statement(m.decision_date)
        if got is None:
            continue
        url, text = got
        p = pr_parsers.parse_boj_statement(text)
        if p["call_rate_target"] is None:
            if re.search(r"guideline\s*for\s*money\s*market\s*operations", text, re.I) and m.scheduled:
                problems.append(f"boj {m.decision_date}: guideline in {url} not read (new regime?)")
            continue
        eff = p["effective"] or effective_date("boj", m.decision_date, cal, lookup)
        lo, hi = p["call_rate_target"]
        cur = rate_in_effect(committed, "call_target_upper", eff - dt.timedelta(days=1))
        if cur is None or math.isnan(cur) or abs(cur - hi) > 1e-9 or \
                abs((rate_in_effect(committed, "call_target_lower", eff - dt.timedelta(days=1)) or 0) - lo) > 1e-9:
            rows += [PolicyRate(eff, "call_target_lower", lo, "primary", url, today_iso()),
                     PolicyRate(eff, "call_target_upper", hi, "primary", url, today_iso()),
                     PolicyRate(eff, "call_target_midpoint", round((lo + hi) / 2, 4), "derived", url, today_iso())]
        if p["cdf_rate"] is not None:
            cur = rate_in_effect(committed, "ioer", eff - dt.timedelta(days=1))
            if cur is None or abs(cur - p["cdf_rate"]) > 1e-9:
                rows.append(PolicyRate(eff, "ioer", p["cdf_rate"], "primary", url, today_iso()))
    return rows, problems
