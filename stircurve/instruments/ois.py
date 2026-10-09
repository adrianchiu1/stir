"""Overnight-index swaps priced from a flat-forward curve (self-discounted).

Conventions come from the manifest entry: spot lag and its calendar, roll
convention, fixed and float leg frequency and day count, payment lag, fixing
calendar and the period schedule (``schedule``: generation, stub, end-of-month).
A tenor up to one year pays once (``short_tenor: single_payment_le_1y``).

Par rate = sum_i P(pay_i) (G_i - 1) / sum_i P(pay_i) tau_i, with G_i the
compounded overnight growth over float period i, tau_i the fixed-leg year
fraction and P the discount factor from the curve itself (``discount: self`` in
usd.yaml). Fixed and float periods coincide (both legs annual for USSO).
"""
from __future__ import annotations

import datetime as dt
from typing import TYPE_CHECKING

import numpy as np

from ..refdata.calendars import add_months, parse_tenor
from ..marketdata.manifest import Manifest
from .daycount import year_fraction
from .futures import BoundInstrument

if TYPE_CHECKING:   # curves import the day counts from this package
    from ..curves.flat_forward import FlatForwardCurve, ParcelGrid

FREQ_MONTHS = {"annual": 12, "semiannual": 6, "quarterly": 3, "monthly": 1}


class OvernightIndexSwap:
    def __init__(self, m: Manifest, instrument: str, tenor: str, as_of: dt.date):
        ins = m.instruments[instrument]
        if ins["kind"] != "swap" or ins["float_leg"]["accrual"] != "compounded":
            raise ValueError(f"{instrument} is not an OIS")
        fixed, flt = ins["fixed_leg"], ins["float_leg"]
        if fixed["frequency"] != flt["frequency"]:
            raise ValueError(f"{instrument}: fixed and float frequencies differ ({fixed['frequency']}, {flt['frequency']})")
        sched = ins.get("schedule")
        if sched is None:
            raise ValueError(f"{instrument}: manifest has no 'schedule' (generation, stub, eom)")
        if (sched["generation"], sched["stub"]) != ("backward", "short_front"):
            raise ValueError(f"{instrument}: schedule {sched} not supported")
        self.instrument, self.contract, self.tenor = instrument, tenor, tenor
        self.as_of = as_of
        self.calendar = m.calendar(flt["fixing_calendar"])
        self.float_daycount = flt["daycount"]
        self.fixed_daycount = fixed["daycount"]
        self.quote = ins["quote"]
        spot_cal = m.calendar(ins["spot_lag"]["calendar"])
        pay_cal = m.calendar(ins["payment_lag"]["calendar"])
        roll = ins["roll"]
        self.spot = spot_cal.advance_business_days(spot_cal.adjust(as_of, "following"), ins["spot_lag"]["days"])
        months, days, weeks = parse_tenor(tenor)
        if days:
            raise ValueError(f"{instrument}: day tenors not supported ({tenor})")
        eom = bool(sched["eom"])
        end_unadj = (self.spot + dt.timedelta(weeks=weeks)) if weeks else self._roll(self.spot, months, eom, spot_cal)
        step = FREQ_MONTHS[fixed["frequency"]]
        single = weeks or (fixed.get("short_tenor") == "single_payment_le_1y" and months <= 12) or months <= step
        bounds = [end_unadj]
        if not single:
            k = 1
            while True:
                d = self._roll(self.spot, months - k * step, eom, spot_cal)
                if d <= self.spot:
                    break
                bounds.append(d)
                k += 1
        unadj = [self.spot] + sorted(bounds)
        adj = [self.spot] + [spot_cal.adjust(d, roll) for d in unadj[1:]]
        self.periods = list(zip(adj[:-1], adj[1:]))
        self.payments = [pay_cal.advance_business_days(e, ins["payment_lag"]["days"]) for _, e in self.periods]
        self.start, self.end = self.spot, adj[-1]

    @staticmethod
    def _roll(spot: dt.date, months: int, eom: bool, cal) -> dt.date:
        d = add_months(spot, months)
        if eom and cal.next_business_day(spot).month != spot.month:     # spot is the month's last business day
            nxt = add_months(dt.date(d.year, d.month, 1), 1)
            d = cal.previous_business_day(nxt)
        return d

    def rate_from_quote(self, q: float) -> float:
        if self.quote["convention"] != "rate":
            raise ValueError(f"unsupported quote convention {self.quote}")
        return q

    def bind(self, grid: ParcelGrid) -> BoundInstrument:
        flt = [grid.rate_days(s, e, self.calendar, self.float_daycount, "business_day") for s, e in self.periods]
        disc = [grid.rate_days(grid.as_of, p, self.calendar, self.float_daycount, "business_day") for p in self.payments]
        tau = np.array([year_fraction(self.fixed_daycount, s, e, self.calendar) for s, e in self.periods])

        def value(x: np.ndarray) -> float:
            p = np.array([1.0 / d.growth(x) for d in disc])
            g = np.array([f.growth(x) for f in flt])
            return float(np.dot(p, g - 1.0) / np.dot(p, tau) * 100.0)

        return BoundInstrument(flt + disc, value)

    def rate(self, curve: FlatForwardCurve) -> float:
        return self.bind(curve.grid).value(curve.rates)
