"""Curve nodes for one as-of date: the meetings whose effective dates open parcels (D2).

* Published meetings (implementation dates already resolved there, D15-D18),
  synthetic meetings from cadence extrapolation to the horizon (flagged, D2).
* Unscheduled decisions enter from their decision date (``front_end.unscheduled:
  from_decision_date``; no look-ahead, D11). A decided meeting whose effective
  date is still ahead is a known step, not a priced one (AC, PR #4).
* A scheduled meeting that an unscheduled decision superseded (``superseded_on``)
  is a node for as-of dates before the supersession only (AC, PR #4).
* A month-end is never a node (D8; AC, PR #4).
"""
from __future__ import annotations

import datetime as dt

import pandas as pd

from ..refdata.meetings import Meeting, MeetingSchedule
from .flat_forward import ParcelGrid


def meeting_nodes(cfg: dict, as_of: dt.date, through: dt.date,
                  schedule: MeetingSchedule | None = None) -> list[Meeting]:
    """Meetings in force on ``as_of`` whose effective date falls in (as_of, through), one per effective date."""
    sched = schedule or MeetingSchedule(cfg["bank"])
    ms = sched.with_synthetic(through, cfg["meetings"]["expected_per_year"])
    rule = cfg["front_end"]["unscheduled"]
    if rule not in ("from_decision_date", "always"):
        raise ValueError(f"front_end.unscheduled {rule!r}")
    keep = [x for x in ms if x.in_force_on(as_of) and (x.scheduled or rule == "always" or x.decision_date <= as_of)]
    out, seen = [], set()
    for x in sorted(keep, key=lambda x: (x.effective_date, x.decision_date)):
        if as_of < x.effective_date < through and x.effective_date not in seen:
            seen.add(x.effective_date)
            out.append(x)
    return out


def node_label(m: Meeting) -> str:
    return m.decision_date.isoformat() + (" (synthetic)" if m.synthetic else "") + ("" if m.scheduled else " (unscheduled)")


def build_grid(as_of: dt.date, meetings: list[Meeting], fixings: pd.Series | dict) -> ParcelGrid:
    """Stub parcel from the as-of date, then one parcel per meeting effective date; past rate dates take the fixings."""
    if isinstance(fixings, pd.Series):
        fx = {pd.Timestamp(d).date(): float(v) for d, v in fixings.dropna().items() if pd.Timestamp(d).date() < as_of}
    else:
        fx = {d: float(v) for d, v in fixings.items() if d < as_of}
    starts = (as_of,) + tuple(x.effective_date for x in meetings)
    return ParcelGrid(as_of, starts, fx, ("stub",) + tuple(node_label(x) for x in meetings))
