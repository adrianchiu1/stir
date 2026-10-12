"""Flat-forward overnight curve between effective dates (D2).

A ``ParcelGrid`` fixes the structure for one as-of date: parcel k is
[starts[k], starts[k+1]) (the last one is open-ended), ``starts[0]`` is the as-of
date, every later start is a meeting's effective date. Rate dates before the as-of
date take the published fixing. A ``FlatForwardCurve`` is a grid plus one
overnight rate (percent) per parcel.

Instruments do not walk the curve day by day at every evaluation: ``rate_days``
maps a window to the rate date each piece of it uses (parcel index, or a fixed
past fixing) once, so pricing is a vectorised lookup ``x[idx]``. Which rate a day
uses follows the instrument's fixing calendar: a non-publication day takes the
rate of the last preceding publication day (FF futures, CBOT Chapter 22; EFFR
OIS compounding over weekends and holidays).
"""
from __future__ import annotations

import bisect
import datetime as dt
from dataclasses import dataclass, field

import numpy as np

from ..instruments.daycount import accrual_factor, year_fraction
from ..refdata.calendars import Calendar

ONE_DAY = dt.timedelta(days=1)
FIXING_LOOKBACK_DAYS = 7      # a past rate date with no fixing on file takes the last fixing this close (reported)


@dataclass(frozen=True)
class RateDays:
    """Pieces of a window: the parcel each uses (-1: a fixed past fixing) and its year fraction."""
    idx: np.ndarray          # int, parcel index or -1
    fixed: np.ndarray        # percent where idx == -1
    weight: np.ndarray       # year fraction of each piece
    daycount: str
    missing: tuple[dt.date, ...] = ()   # past rate dates with no fixing on file

    def values(self, x: np.ndarray) -> np.ndarray:
        """Rate (percent) of each piece under parcel rates ``x``."""
        return np.where(self.idx >= 0, x[np.maximum(self.idx, 0)], self.fixed)

    def average(self, x: np.ndarray) -> float:
        """Day-count weighted arithmetic average (percent)."""
        return float(np.dot(self.weight, self.values(x)) / self.weight.sum())

    def growth(self, x: np.ndarray) -> float:
        """Compounded growth of 1 over the window."""
        r = self.values(x) / 100.0
        return float(np.prod([accrual_factor(self.daycount, ri, wi) for ri, wi in zip(r, self.weight)])
                     if self.daycount == "BUS/252" else np.prod(1.0 + r * self.weight))

    def compounded(self, x: np.ndarray) -> float:
        """Compounded rate over the window (percent, the day count's simple annualisation)."""
        return (self.growth(x) - 1.0) / self.weight.sum() * 100.0


@dataclass
class ParcelGrid:
    as_of: dt.date
    starts: tuple[dt.date, ...]
    fixings: dict[dt.date, float] = field(default_factory=dict)   # rate date -> percent
    labels: tuple[str, ...] = ()                                    # per parcel, for reports

    def __post_init__(self):
        if not self.starts or self.starts[0] != self.as_of:
            raise ValueError("the first parcel starts on the as-of date")
        if any(b <= a for a, b in zip(self.starts, self.starts[1:])):
            raise ValueError("parcel starts must increase")
        self._fix_dates = sorted(self.fixings)

    @property
    def n(self) -> int:
        return len(self.starts)

    def parcel_of(self, day: dt.date) -> int:
        if day < self.as_of:
            raise ValueError(f"{day} is before the as-of date {self.as_of}")
        return bisect.bisect_right(self.starts, day) - 1

    def ends(self, last: dt.date) -> list[dt.date]:
        """Parcel ends (exclusive), the last one closed at ``last``."""
        return list(self.starts[1:]) + [last]

    def _past(self, rd: dt.date) -> tuple[int, float, bool]:
        if rd in self.fixings:
            return -1, self.fixings[rd], False
        i = bisect.bisect_left(self._fix_dates, rd) - 1
        if i >= 0 and (rd - self._fix_dates[i]).days <= FIXING_LOOKBACK_DAYS:
            return -1, self.fixings[self._fix_dates[i]], True
        return 0, np.nan, True       # nothing close on file: the stub parcel stands in (reported)

    def rate_days(self, start: dt.date, end: dt.date, calendar: Calendar, daycount: str,
                  per: str = "calendar_day") -> RateDays:
        """Pieces of [start, end) and the rate date each uses on ``calendar``.

        ``per='calendar_day'``: one piece per calendar day (arithmetic averages);
        ``per='business_day'``: one piece per business day running to the next one
        (daily compounding; a window opening on a holiday starts with a piece at the
        previous business day's rate)."""
        if per == "calendar_day":
            cuts = [start + dt.timedelta(days=i) for i in range((end - start).days)]
        elif per == "business_day":
            cuts = [start] + [d for d in calendar.business_days(start + ONE_DAY, end - ONE_DAY)]
        else:
            raise ValueError(f"unknown piece {per!r}")
        nxt = cuts[1:] + [end]
        idx, fixed, weight, missing = [], [], [], []
        for a, b in zip(cuts, nxt):
            rd = calendar.previous_business_day(a, include=True)
            if rd < self.as_of:
                i, v, miss = self._past(rd)
                if miss:
                    missing.append(rd)
            else:
                i, v = self.parcel_of(rd), np.nan
            idx.append(i)
            fixed.append(v)
            weight.append(year_fraction(daycount, a, b, calendar))
        return RateDays(np.array(idx, dtype=int), np.array(fixed, dtype=float), np.array(weight, dtype=float),
                        daycount, tuple(sorted(set(missing))))


@dataclass
class FlatForwardCurve:
    grid: ParcelGrid
    rates: np.ndarray        # percent, one per parcel

    def __post_init__(self):
        self.rates = np.asarray(self.rates, dtype=float)
        if self.rates.shape != (self.grid.n,):
            raise ValueError(f"{self.grid.n} parcels, {self.rates.shape} rates")

    def rate_on(self, day: dt.date, calendar: Calendar) -> float:
        """Overnight rate (percent) applying on ``day``: the fixing for past rate dates,
        else the parcel rate of the last publication day on or before it."""
        rd = calendar.previous_business_day(day, include=True)
        if rd < self.grid.as_of:
            i, v, _ = self.grid._past(rd)
            return v if i < 0 else float(self.rates[i])
        return float(self.rates[self.grid.parcel_of(rd)])

    def discount(self, t: dt.date, calendar: Calendar, daycount: str) -> float:
        """Discount factor from the as-of date to ``t`` compounding the overnight rate."""
        if t <= self.grid.as_of:
            return 1.0
        return 1.0 / self.grid.rate_days(self.grid.as_of, t, calendar, daycount, "business_day").growth(self.rates)
