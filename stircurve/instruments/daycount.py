"""Day-count conventions by name (the manifest names them; nothing here assumes one).

``year_fraction(name, start, end, calendar)`` for [start, end). ``BUS/252`` counts
business days of ``calendar`` and compounds exponentially (BRL); the ACT and 30/360
conventions accrue simply.
"""
from __future__ import annotations

import datetime as dt

from ..refdata.calendars import Calendar

SIMPLE = ("ACT/360", "ACT/365F", "ACT/365", "30/360")
EXPONENTIAL = ("BUS/252",)


def year_fraction(name: str, start: dt.date, end: dt.date, calendar: Calendar | None = None) -> float:
    if name == "ACT/360":
        return (end - start).days / 360.0
    if name in ("ACT/365F", "ACT/365"):
        return (end - start).days / 365.0
    if name == "30/360":           # US (bond basis)
        d1, d2 = min(start.day, 30), end.day
        if d1 == 30 and d2 == 31:
            d2 = 30
        return (360 * (end.year - start.year) + 30 * (end.month - start.month) + (d2 - d1)) / 360.0
    if name == "BUS/252":
        if calendar is None:
            raise ValueError("BUS/252 needs a calendar")
        return calendar.business_days_between(start, end) / 252.0
    raise ValueError(f"unknown day count {name!r}")


def accrual_factor(name: str, rate: float, yf: float) -> float:
    """Growth of 1 over ``yf`` years at ``rate`` (decimal) under the convention's compounding."""
    if name in EXPONENTIAL:
        return (1.0 + rate) ** yf
    if name in SIMPLE:
        return 1.0 + rate * yf
    raise ValueError(f"unknown day count {name!r}")
