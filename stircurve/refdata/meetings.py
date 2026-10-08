"""Central-bank meeting schedules and the parcels they define.

File: ``data/refdata/meetings/<bank>.csv`` with columns
``decision_date, effective_date, scheduled, regime, synthetic, source_url, retrieved_at``.
Unscheduled decisions live in ``<bank>_unscheduled.csv`` with the same columns.

Effective-date rules (see the design spec, "Reference data"):

* fed: decision date + 1 business day on the ``us_fed`` calendar.
* ecb: start of the reserve maintenance period attached to the meeting in
  ``data/refdata/maintenance_periods/ecb.csv``; rule-based fallback for
  synthetic meetings (Wednesday after a Thursday decision, rolled forward
  over TARGET closing days).
* boe: the decision date itself.
* boj: next business day on the ``jp`` calendar (D15).

For every bank a published implementation date wins over the rule: the ECB
maintenance-period table, and ``meetings/published_effective.csv`` for
individual decisions (e.g. BoJ 29 Jan 2016 -> 16 Feb 2016).

Cadence extrapolation reproduces each bank's rhythm beyond the published
horizon by replicating the (month, ordinal weekday-of-month, weekday) slots
of the latest fully published calendar year. Synthetic rows are flagged.
"""
from __future__ import annotations

import csv
import datetime as dt
from dataclasses import dataclass
from pathlib import Path

from .. import REFDATA_DIR
from .calendars import Calendar

BANKS = ("fed", "ecb", "boe", "boj")
BANK_CALENDAR = {"fed": "us_fed", "ecb": "target", "boe": "uk", "boj": "jp"}
COLUMNS = ["decision_date", "effective_date", "scheduled", "regime", "synthetic", "source_url", "retrieved_at"]


@dataclass(frozen=True)
class Meeting:
    bank: str
    decision_date: dt.date
    effective_date: dt.date
    scheduled: bool = True
    regime: str = ""
    synthetic: bool = False
    source_url: str = ""
    retrieved_at: str = ""

    def as_row(self) -> dict:
        return {
            "decision_date": self.decision_date.isoformat(),
            "effective_date": self.effective_date.isoformat(),
            "scheduled": int(self.scheduled),
            "regime": self.regime,
            "synthetic": int(self.synthetic),
            "source_url": self.source_url,
            "retrieved_at": self.retrieved_at,
        }


@dataclass(frozen=True)
class Parcel:
    """A period over which the overnight rate is assumed flat."""
    start: dt.date          # inclusive
    end: dt.date            # exclusive
    decision_date: dt.date | None   # meeting whose effective date opens the parcel (None = stub)
    synthetic: bool


# ---------------------------------------------------------------------------
# io
# ---------------------------------------------------------------------------
def _parse_bool(v: str) -> bool:
    return str(v).strip().lower() in ("1", "true", "t", "yes", "y")


def meetings_path(bank: str, unscheduled: bool = False, refdata_dir: Path = REFDATA_DIR) -> Path:
    suffix = "_unscheduled" if unscheduled else ""
    return refdata_dir / "meetings" / f"{bank}{suffix}.csv"


def load_meetings(bank: str, include_unscheduled: bool = True,
                  refdata_dir: Path = REFDATA_DIR) -> list[Meeting]:
    out: list[Meeting] = []
    for unsched in (False, True) if include_unscheduled else (False,):
        p = meetings_path(bank, unsched, refdata_dir)
        if not p.exists():
            continue
        with p.open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if not row.get("decision_date"):
                    continue
                out.append(Meeting(
                    bank=bank,
                    decision_date=dt.date.fromisoformat(row["decision_date"]),
                    effective_date=dt.date.fromisoformat(row["effective_date"]),
                    scheduled=_parse_bool(row.get("scheduled", "1")),
                    regime=row.get("regime", ""),
                    synthetic=_parse_bool(row.get("synthetic", "0")),
                    source_url=row.get("source_url", ""),
                    retrieved_at=row.get("retrieved_at", ""),
                ))
    return sorted(out, key=lambda m: m.decision_date)


def save_meetings(bank: str, meetings: list[Meeting], unscheduled: bool = False,
                  refdata_dir: Path = REFDATA_DIR) -> Path:
    p = meetings_path(bank, unscheduled, refdata_dir)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        for m in sorted(meetings, key=lambda m: m.decision_date):
            w.writerow(m.as_row())
    return p


# ---------------------------------------------------------------------------
# effective-date rules
# ---------------------------------------------------------------------------
def effective_date(bank: str, decision: dt.date, calendar: Calendar,
                   published: dict[dt.date, dt.date] | None = None) -> dt.date:
    """Date on which a decision taken on ``decision`` applies to the overnight rate.

    A published implementation date (``published``: decision -> effective, see
    ``published_lookup``) always wins; the bank's rule is the fallback.
    """
    if published and decision in published:
        return published[decision]
    if bank == "fed":
        return calendar.next_business_day(decision)
    if bank == "boe":
        return decision
    if bank == "boj":
        return calendar.next_business_day(decision)
    if bank == "ecb":
        return ecb_rule_effective(decision, calendar)
    raise ValueError(f"unknown bank {bank!r}")


PUBLISHED_COLUMNS = ["bank", "decision_date", "effective_date", "source_url", "note"]


def published_path(refdata_dir: Path = REFDATA_DIR) -> Path:
    return refdata_dir / "meetings" / "published_effective.csv"


def load_published_effective(bank: str, refdata_dir: Path = REFDATA_DIR) -> dict[dt.date, tuple[dt.date, str]]:
    """Implementation dates published for individual decisions where they are
    not the rule's (BoJ 29 Jan 2016) or where AC asked for the published date to
    be recorded (Fed 3 Mar 2020): decision -> (effective, source_url)."""
    p = published_path(refdata_dir)
    if not p.exists():
        return {}
    out = {}
    with p.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row.get("bank") == bank and row.get("decision_date"):
                if not row.get("source_url"):
                    raise ValueError(f"{p}: {row['decision_date']} has no source_url")
                out[dt.date.fromisoformat(row["decision_date"])] = (dt.date.fromisoformat(row["effective_date"]),
                                                                    row["source_url"])
    return out


# A rate change is the published implementation date of the latest decision up to
# this many calendar days before it (Japan: holiday clusters, 18 -> 24 Sep 2026).
RATE_CHANGE_WINDOW_DAYS = {"fed": 3, "boj": 7}
RATE_CHANGE_ANCHORS = {"fed": ("target_upper",),
                       "boj": ("call_target_upper", "ioer", "policy_rate_balance_rate", "basic_loan_rate")}


def published_from_rate_changes(decisions: list[dt.date], change_dates: list[dt.date],
                                window_days: int = 3) -> dict[dt.date, dt.date]:
    """Each policy-rate change dates when a decision took effect: the latest
    decision on or up to ``window_days`` before it. Fed: the open-market table
    (FRED DFEDTAR before 2003) — the decision day until 2008, the next business
    day since 2015. BoJ: statements and the basic loan rate CSV — 'effective
    immediately' 2006-2010, the next business day since 2024."""
    ds = sorted(set(decisions))
    out = {}
    for c in sorted(set(change_dates)):
        cands = [d for d in ds if 0 <= (c - d).days <= window_days]
        if cands:
            out[cands[-1]] = c
    return out


fed_published_from_rates = published_from_rate_changes   # name used in earlier tests


def published_lookup(bank: str, refdata_dir: Path = REFDATA_DIR,
                     decisions: list[dt.date] | None = None) -> dict[dt.date, dt.date]:
    """decision -> published implementation date: the ECB maintenance-period
    table; for the Fed and the BoJ the change dates of the policy-rate history
    matched to ``decisions`` (default: committed meetings); then
    ``published_effective.csv`` (which wins on a clash)."""
    out: dict[dt.date, dt.date] = {}
    if bank == "ecb":
        from .maintenance import load_maintenance_periods, mp_lookup   # local import: maintenance imports meetings lazily
        out.update(mp_lookup(load_maintenance_periods(refdata_dir)))
    if bank in RATE_CHANGE_ANCHORS:
        from .maintenance import load_policy_rates
        if decisions is None:
            decisions = [m.decision_date for m in load_meetings(bank, True, refdata_dir)]
        rates = load_policy_rates(bank, refdata_dir)
        changes = [r.effective_date for i, r in enumerate(rates) if r.anchor in RATE_CHANGE_ANCHORS[bank]
                   and r.effective_date >= min(decisions, default=r.effective_date)]
        out.update(published_from_rate_changes(decisions, changes, RATE_CHANGE_WINDOW_DAYS[bank]))
    out.update({d: eff for d, (eff, _) in load_published_effective(bank, refdata_dir).items()})
    return out


def ecb_rule_effective(decision: dt.date, target: Calendar) -> dt.date:
    """Fallback for the 2004+ regime: the maintenance period starts on the
    settlement day of the MRO following the meeting — the Wednesday after a
    Thursday meeting, rolled forward if TARGET is closed. The ECB's published
    table overrides this (e.g. MP 3/2027 starts Thu 6 May 2027)."""
    wed = decision + dt.timedelta(days=(2 - decision.weekday()) % 7 or 7)  # next Wednesday strictly after
    return target.next_business_day(wed, include=True)


# ---------------------------------------------------------------------------
# cadence extrapolation
# ---------------------------------------------------------------------------
def _slot(d: dt.date) -> tuple[int, int, int]:
    """(month, ordinal weekday-of-month, weekday). Ordinal counts occurrences
    of that weekday in the month up to and including ``d``."""
    return d.month, (d.day - 1) // 7 + 1, d.weekday()


def _date_from_slot(year: int, slot: tuple[int, int, int]) -> dt.date:
    month, ordinal, weekday = slot
    first = dt.date(year, month, 1)
    offset = (weekday - first.weekday()) % 7
    d = first + dt.timedelta(days=offset + 7 * (ordinal - 1))
    if d.month != month:          # 5th occurrence missing this year -> use 4th
        d -= dt.timedelta(days=7)
    return d


def template_year(meetings: list[Meeting], expected_count: int) -> int | None:
    """Latest calendar year with at least ``expected_count`` published,
    scheduled, non-synthetic meetings."""
    years: dict[int, int] = {}
    for m in meetings:
        if m.scheduled and not m.synthetic:
            years[m.decision_date.year] = years.get(m.decision_date.year, 0) + 1
    ok = [y for y, n in years.items() if n >= expected_count]
    return max(ok) if ok else None


def extrapolate_cadence(bank: str, meetings: list[Meeting], through: dt.date,
                        calendar: Calendar, published: dict[dt.date, dt.date] | None = None,
                        expected_count: int = 8) -> list[Meeting]:
    """Return published meetings plus synthetic ones through ``through``.

    Synthetic decision dates replicate the template year's slots; a date that
    lands on a holiday of the bank's calendar moves to the next business day.
    """
    published = [m for m in meetings if not m.synthetic]
    ty = template_year(published, expected_count)
    if ty is None:
        raise ValueError(f"{bank}: no complete published year to use as cadence template")
    slots = sorted(_slot(m.decision_date) for m in published
                   if m.decision_date.year == ty and m.scheduled)
    last_published = max(m.decision_date for m in published if m.scheduled)
    out = list(published)
    year = last_published.year
    while True:
        year += 1
        new = []
        for s in slots:
            d = _date_from_slot(year, s)
            d = calendar.next_business_day(d, include=True)
            if d <= last_published:
                continue
            new.append(Meeting(bank, d, effective_date(bank, d, calendar, published),
                               scheduled=True, regime="synthetic", synthetic=True,
                               source_url=f"cadence-template:{ty}"))
        # also fill any gap in the current year after the last published meeting
        if year == last_published.year + 1:
            for s in slots:
                d = _date_from_slot(last_published.year, s)
                d = calendar.next_business_day(d, include=True)
                if d > last_published and all(abs((d - m.decision_date).days) > 3 for m in published):
                    new.append(Meeting(bank, d, effective_date(bank, d, calendar, published),
                                       scheduled=True, regime="synthetic", synthetic=True,
                                       source_url=f"cadence-template:{ty}"))
        out.extend(m for m in new if m.decision_date <= through)
        if year >= through.year:
            break
    return sorted(out, key=lambda m: m.decision_date)


# ---------------------------------------------------------------------------
# parcels
# ---------------------------------------------------------------------------
def parcels(meetings: list[Meeting], start: dt.date, end: dt.date) -> list[Parcel]:
    """Flat-rate periods between effective dates covering [start, end).

    The first parcel runs from ``start`` to the first effective date after
    it (a stub keyed to no decision); each later parcel opens on an
    effective date and closes on the next one, the last at ``end``.
    """
    eff = sorted({m.effective_date: m for m in meetings if start < m.effective_date < end}.items())
    out: list[Parcel] = []
    cur, cur_m = start, None
    for d, m in eff:
        out.append(Parcel(cur, d, cur_m.decision_date if cur_m else None,
                          cur_m.synthetic if cur_m else False))
        cur, cur_m = d, m
    out.append(Parcel(cur, end, cur_m.decision_date if cur_m else None,
                      cur_m.synthetic if cur_m else False))
    return out


class MeetingSchedule:
    """Convenience wrapper: published + unscheduled + synthetic meetings for one bank."""

    def __init__(self, bank: str, calendar: Calendar | None = None,
                 mp_lookup: dict[dt.date, dt.date] | None = None,
                 refdata_dir: Path = REFDATA_DIR):
        self.bank = bank
        self.calendar = calendar or Calendar.load(BANK_CALENDAR[bank], refdata_dir=refdata_dir)
        self.mp_lookup = mp_lookup if mp_lookup is not None else published_lookup(bank, refdata_dir)
        self.published = load_meetings(bank, include_unscheduled=True, refdata_dir=refdata_dir)

    def with_synthetic(self, through: dt.date, expected_count: int = 8) -> list[Meeting]:
        return extrapolate_cadence(self.bank, self.published, through, self.calendar,
                                   self.mp_lookup, expected_count)

    def parcels(self, as_of: dt.date, horizon_years: int = 3) -> list[Parcel]:
        end = dt.date(as_of.year + horizon_years, as_of.month, min(as_of.day, 28))
        ms = self.with_synthetic(end)
        return parcels(ms, as_of, end)

    def next_meetings(self, as_of: dt.date, n: int = 12) -> list[Meeting]:
        ms = self.with_synthetic(dt.date(as_of.year + 3, 12, 31))
        return [m for m in ms if m.decision_date >= as_of][:n]
