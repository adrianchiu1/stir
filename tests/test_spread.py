"""Policy spread estimator (D7) on SYNTHETIC fixings (made-up numbers, real calendar and anchors)."""
import datetime as dt

import numpy as np
import pandas as pd

from stircurve.policy.spread import policy_spread, turn_days, turn_effects, winsorised_mean
from stircurve.refdata.calendars import Calendar
from stircurve.refdata.maintenance import PolicyRate, load_policy_rates

D = dt.date
FED = Calendar.load("us_fed")
RATES = load_policy_rates("fed")


def _window(as_of, n=63):
    days, d = [], FED.previous_business_day(as_of)
    while len(days) < n:
        days.append(d)
        d = FED.previous_business_day(d)
    return sorted(days)


def test_turn_days_are_month_end_business_days():
    t = turn_days(FED, D(2024, 1, 1), D(2024, 12, 31))
    assert D(2024, 3, 29) in t                     # Good Friday is a us_fed business day
    assert D(2024, 8, 30) in t and D(2024, 11, 29) in t and D(2024, 12, 31) in t and len(t) == 12
    assert turn_days(FED, D(2024, 1, 1), D(2024, 12, 31), ("quarter_end",)) == {
        D(2024, 3, 29), D(2024, 6, 28), D(2024, 9, 30), D(2024, 12, 31)}


def test_winsorised_mean_and_median_with_turns_dropped():
    """2024-08-14 as-of: midpoint 5.375 throughout; spread 8bp with noise, month-ends -10bp
    (dropped), two outliers (+50bp, -40bp) clipped by the 10/90 winsorisation."""
    as_of = D(2024, 8, 14)
    days = _window(as_of)
    turns = turn_days(FED, days[0], days[-1])
    rng = np.random.default_rng(7)
    noise = rng.integers(-2, 3, len(days)) / 100.0
    fx = {}
    for d, e in zip(days, noise):
        fx[d] = 5.375 + 0.08 + e + (-0.10 if d in turns else 0.0)
    fx[days[10]] += 0.50
    fx[days[20]] -= 0.40
    est = policy_spread(pd.Series(fx), RATES, "target_midpoint", FED, as_of)
    keep = np.array([fx[d] - 5.375 for d in days if d not in turns])
    assert est.n_obs == len(keep) == 63 - len(turns) and est.n_turn_dropped == len(turns) == 3
    lo, hi = np.quantile(keep, [0.1, 0.9])
    assert abs(est.value - np.clip(keep, lo, hi).mean()) < 1e-12
    assert abs(est.median - np.median(keep)) < 1e-12
    assert abs(est.value - 0.08) < 0.01 and est.window == (days[0], days[-1])
    med = policy_spread(pd.Series(fx), RATES, "target_midpoint", FED, as_of, estimator="median")
    assert med.value == med.median


def test_anchor_in_effect_changes_inside_the_window():
    """Window spans the 18 Sep 2024 cut (effective 19 Sep): EFFR follows the new midpoint."""
    as_of = D(2024, 10, 15)
    days = _window(as_of)
    fx = {d: (5.375 if d < D(2024, 9, 19) else 4.875) + 0.08 for d in days}
    est = policy_spread(pd.Series(fx), RATES, "target_midpoint", FED, as_of)
    assert abs(est.value - 0.08) < 1e-12 and abs(est.median - 0.08) < 1e-12


def test_too_few_fixings_give_no_spread():
    as_of = D(2024, 8, 14)
    fx = {d: 5.455 for d in _window(as_of)[-5:]}
    est = policy_spread(pd.Series(fx), RATES, "target_midpoint", FED, as_of)
    assert est.value is None and est.n_obs == 5 and "< 20" in est.note and est.n_missing == 58


def test_turn_effects_measure_month_end_dips():
    days = FED.business_days(D(2023, 1, 3), D(2023, 12, 29))
    me = turn_days(FED, days[0], days[-1])
    fx = {d: (5.08 if d < D(2023, 2, 2) else 5.33) + (-0.03 if d in me else 0.0) for d in days}
    rates = [PolicyRate(D(2022, 12, 15), "target_midpoint", 4.375), PolicyRate(D(2023, 2, 2), "target_midpoint", 4.625)]
    # (synthetic anchors: spread is 70bp all year, month-ends 3bp lower)
    t = turn_effects(pd.Series(fx), rates, "target_midpoint", FED)
    turn = t[t["day"] == "turn"]
    assert set(turn["kind"]) == {"month_end", "quarter_end", "year_end"}
    assert np.allclose(turn["mean"], -3.0)
    assert np.allclose(t[t["day"] == "after"]["mean"], 0.0)
    assert winsorised_mean(np.array([0.0, 1.0, 2.0, 3.0, 100.0]), 0.0, 0.8) == np.mean([0, 1, 2, 3, np.quantile([0, 1, 2, 3, 100], 0.8)])
