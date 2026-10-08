"""ECB reserve maintenance periods and policy-rate schedules.

Maintenance periods: ``data/refdata/maintenance_periods/ecb.csv`` with columns
``mp_label, meeting_decision_date, mp_start, mp_end, source_url, retrieved_at``.
The ECB's annual "indicative operational calendars" press releases are the
authoritative source (see parsers/ecb.py). Three regimes exist:

* 1999 – 9 Mar 2004: MPs ran from the 24th of a month to the 23rd of the next;
  rate changes did not align with MP starts. Encoded only through the table.
* 10 Mar 2004 – Dec 2014: MP starts on the settlement day of the MRO after the
  first Governing Council meeting of the month (monthly).
* 2015 –: eight MPs a year, aligned with the six-weekly monetary-policy meetings.

Policy rates: ``data/refdata/policy_rates/<bank>.csv`` with columns
``effective_date, anchor, rate, source_url, retrieved_at``. ``anchor`` names the
instrument (fed: target_upper, target_lower, target_midpoint, iorb, ioer;
ecb: dfr, mro, mlf; boe: bank_rate; boj: call_target_lower/upper/midpoint,
ioer (complementary deposit facility), policy_rate_balance_rate,
basic_loan_rate). A NaN rate means the instrument was not a target then
(BoJ call rate under quantitative easing). ``rate_in_effect`` returns the
level applying on a given day, which drives the spread estimator.
"""
from __future__ import annotations

import csv
import datetime as dt
from dataclasses import dataclass
from pathlib import Path

from .. import REFDATA_DIR
from .calendars import Calendar

MP_COLUMNS = ["mp_label", "meeting_decision_date", "mp_start", "mp_end", "source_url", "retrieved_at"]
PR_COLUMNS = ["effective_date", "anchor", "rate", "confidence", "source_url", "retrieved_at"]


@dataclass(frozen=True)
class MaintenancePeriod:
    label: str
    meeting_decision_date: dt.date | None
    start: dt.date          # inclusive
    end: dt.date            # inclusive (ECB convention); exclusive end = end + 1 day
    source_url: str = ""
    retrieved_at: str = ""

    @property
    def end_exclusive(self) -> dt.date:
        return self.end + dt.timedelta(days=1)

    @property
    def length_days(self) -> int:
        return (self.end - self.start).days + 1


def mp_path(refdata_dir: Path = REFDATA_DIR) -> Path:
    return refdata_dir / "maintenance_periods" / "ecb.csv"


def load_maintenance_periods(refdata_dir: Path = REFDATA_DIR) -> list[MaintenancePeriod]:
    p = mp_path(refdata_dir)
    if not p.exists():
        return []
    out = []
    with p.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if not row.get("mp_start"):
                continue
            md = row.get("meeting_decision_date") or ""
            out.append(MaintenancePeriod(
                label=row.get("mp_label", ""),
                meeting_decision_date=dt.date.fromisoformat(md) if md else None,
                start=dt.date.fromisoformat(row["mp_start"]),
                end=dt.date.fromisoformat(row["mp_end"]),
                source_url=row.get("source_url", ""),
                retrieved_at=row.get("retrieved_at", ""),
            ))
    return sorted(out, key=lambda m: m.start)


def save_maintenance_periods(mps: list[MaintenancePeriod], refdata_dir: Path = REFDATA_DIR) -> Path:
    p = mp_path(refdata_dir)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(MP_COLUMNS)
        for m in sorted(mps, key=lambda m: m.start):
            w.writerow([m.label, m.meeting_decision_date.isoformat() if m.meeting_decision_date else "",
                        m.start.isoformat(), m.end.isoformat(), m.source_url, m.retrieved_at])
    return p


def mp_lookup(mps: list[MaintenancePeriod]) -> dict[dt.date, dt.date]:
    """decision date -> MP start, for use as ``effective_date`` lookup."""
    return {m.meeting_decision_date: m.start for m in mps if m.meeting_decision_date}


def validate_maintenance_periods(mps: list[MaintenancePeriod]) -> list[str]:
    """Return human-readable problems: gaps, overlaps, implausible lengths."""
    problems = []
    for a, b in zip(mps, mps[1:]):
        if b.start != a.end_exclusive:
            problems.append(f"gap/overlap between {a.label} ending {a.end} and {b.label} starting {b.start}")
    for m in mps:
        if not (7 <= m.length_days <= 70):
            problems.append(f"{m.label}: implausible length {m.length_days} days")
        if m.meeting_decision_date and not (0 < (m.start - m.meeting_decision_date).days <= 14):
            problems.append(f"{m.label}: start {m.start} not within 14 days after meeting {m.meeting_decision_date}")
    return problems


def synthetic_maintenance_periods(decisions: list[dt.date], target: Calendar,
                                  last_known_end: dt.date | None = None) -> list[MaintenancePeriod]:
    """Rule-based MPs for synthetic meetings: start = Wednesday after a
    Thursday decision (rolled over TARGET closures), end = day before next start."""
    from .meetings import ecb_rule_effective  # local import to avoid a cycle
    starts = [ecb_rule_effective(d, target) for d in decisions]
    out = []
    for i, (d, s) in enumerate(zip(decisions, starts)):
        end = (starts[i + 1] - dt.timedelta(days=1)) if i + 1 < len(starts) else None
        if end is None:
            continue
        out.append(MaintenancePeriod(f"synthetic-{d.isoformat()}", d, s, end, "rule:ecb_wednesday_after"))
    return out


# ---------------------------------------------------------------------------
# policy rates
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class PolicyRate:
    effective_date: dt.date
    anchor: str
    rate: float
    confidence: str = "primary"     # primary | derived | memory:<how to verify>
    source_url: str = ""
    retrieved_at: str = ""


def load_policy_rates(bank: str, refdata_dir: Path = REFDATA_DIR) -> list[PolicyRate]:
    p = refdata_dir / "policy_rates" / f"{bank}.csv"
    if not p.exists():
        return []
    out = []
    with p.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if not row.get("effective_date"):
                continue
            out.append(PolicyRate(dt.date.fromisoformat(row["effective_date"]), row["anchor"],
                                  float(row["rate"]), row.get("confidence", "primary"),
                                  row.get("source_url", ""), row.get("retrieved_at", "")))
    return sorted(out, key=lambda r: (r.anchor, r.effective_date))


def save_policy_rates(bank: str, rates: list[PolicyRate], refdata_dir: Path = REFDATA_DIR) -> Path:
    p = refdata_dir / "policy_rates" / f"{bank}.csv"
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(PR_COLUMNS)
        for r in sorted(rates, key=lambda r: (r.anchor, r.effective_date)):
            w.writerow([r.effective_date.isoformat(), r.anchor, r.rate, r.confidence, r.source_url, r.retrieved_at])
    return p


def rate_in_effect(rates: list[PolicyRate], anchor: str, day: dt.date) -> float | None:
    """Level of ``anchor`` applying on ``day`` (last change on or before)."""
    level = None
    for r in rates:
        if r.anchor != anchor:
            continue
        if r.effective_date <= day:
            level = r.rate
        else:
            break
    return level
