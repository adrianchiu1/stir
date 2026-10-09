"""Policy spread (D7): fixing minus the policy anchor in effect.

spread_t = fixing_t - anchor in effect on t, over the trailing ``window_bd``
business days of the fixing calendar ending on the last rate date before the
as-of date (EFFR for day t is published on t+1, so the as-of day's own rate is
not known at its close), turn days dropped, then a winsorised mean (the
``winsor`` quantiles; D7) or the median (the alternative).

Turn days: ``month_end`` is the last business day of each month on the fixing
calendar (which covers quarter- and year-ends); ``quarter_end`` and
``year_end`` restrict to those months. ``turn_effects`` measures them in the
data (evidence for D8: does EFFR need a turn node?).
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

import numpy as np
import pandas as pd

from ..refdata.calendars import Calendar
from ..refdata.maintenance import PolicyRate, rate_in_effect

TURN_MONTHS = {"month_end": range(1, 13), "quarter_end": (3, 6, 9, 12), "year_end": (12,)}


@dataclass
class SpreadEstimate:
    value: float | None          # percent; the configured estimator (None: too few observations)
    winsorised_mean: float | None
    median: float | None
    n_obs: int
    n_turn_dropped: int
    n_missing: int               # business days in the window with no fixing on file
    window: tuple[dt.date, dt.date] | None
    estimator: str
    anchor: str
    note: str = ""


def turn_days(calendar: Calendar, start: dt.date, end: dt.date, kinds=("month_end",)) -> set[dt.date]:
    """Turn days in [start, end] (last business day of the months the kinds name)."""
    months = set()
    for k in kinds:
        months |= set(TURN_MONTHS[k])
    out = set()
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        if m in months:
            nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
            d = calendar.previous_business_day(nxt)
            if start <= d <= end:
                out.add(d)
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def winsorised_mean(v: np.ndarray, lo: float, hi: float) -> float:
    a, b = np.quantile(v, [lo, hi])
    return float(np.clip(v, a, b).mean())


def policy_spread(fixings: pd.Series, rates: list[PolicyRate], anchor: str, calendar: Calendar, as_of: dt.date,
                  window_bd: int = 63, turns=("month_end",), estimator: str = "winsorised_mean",
                  winsor=(0.10, 0.90), min_obs: int = 20) -> SpreadEstimate:
    """``fixings``: percent indexed by rate date (datetime-like)."""
    fx = {pd.Timestamp(d).date(): float(v) for d, v in fixings.dropna().items()}
    last = calendar.previous_business_day(as_of)
    days = []
    d = last
    while len(days) < window_bd:
        days.append(d)
        d = calendar.previous_business_day(d)
    days.reverse()
    turn = turn_days(calendar, days[0], days[-1], turns)
    obs, n_turn, n_missing = [], 0, 0
    for d in days:
        if d not in fx:
            n_missing += 1
            continue
        if d in turn:
            n_turn += 1
            continue
        a = rate_in_effect(rates, anchor, d)
        if a is None:
            continue
        obs.append(fx[d] - a)
    v = np.array(obs)
    if len(v) < min_obs:
        return SpreadEstimate(None, None, None, len(v), n_turn, n_missing, (days[0], days[-1]), estimator, anchor,
                              f"{len(v)} fixings in the window (< {min_obs})")
    wm, med = winsorised_mean(v, *winsor), float(np.median(v))
    value = {"winsorised_mean": wm, "median": med}[estimator]
    return SpreadEstimate(value, wm, med, len(v), n_turn, n_missing, (days[0], days[-1]), estimator, anchor)


def turn_effects(fixings: pd.Series, rates: list[PolicyRate], anchor: str, calendar: Calendar) -> pd.DataFrame:
    """Per year: mean and count of (fixing - anchor) minus the median of the surrounding
    non-turn days, on month-, quarter- and year-end days and on the business day after.
    Each turn day is compared with the median spread of the 10 business days before it
    (non-turn), so level shifts from policy moves cancel. Units: bp."""
    fx = {pd.Timestamp(d).date(): float(v) for d, v in fixings.dropna().items()}
    if not fx:
        return pd.DataFrame()
    first, last = min(fx), max(fx)
    sp = {}
    for d, v in fx.items():
        a = rate_in_effect(rates, anchor, d)
        if a is not None:
            sp[d] = (v - a) * 100.0
    me = turn_days(calendar, first, last, ("month_end",))
    rows = []
    for d in sorted(me):
        ref, x = [], d
        while len(ref) < 10:
            x = calendar.previous_business_day(x)
            if x < first:
                break
            if x in sp and x not in me:
                ref.append(sp[x])
        if d not in sp or len(ref) < 5:
            continue
        base = float(np.median(ref))
        kind = "year_end" if d.month == 12 else "quarter_end" if d.month in (3, 6, 9) else "month_end"
        rows.append({"year": d.year, "kind": kind, "day": "turn", "effect_bp": sp[d] - base})
        nx = calendar.next_business_day(d)
        if nx in sp:
            rows.append({"year": d.year, "kind": kind, "day": "after", "effect_bp": sp[nx] - base})
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return (df.groupby(["year", "kind", "day"])["effect_bp"].agg(["mean", "min", "max", "count"])
            .round(2).reset_index())
