"""Instrument models from the manifest, checked by hand and against Bloomberg's WIRP examples."""
import datetime as dt

import numpy as np

from stircurve.curves.flat_forward import FlatForwardCurve, ParcelGrid
from stircurve.instruments import AverageRateFuture, OvernightIndexSwap, year_fraction
from stircurve.marketdata.contracts import listed_contracts
from stircurve.marketdata.manifest import load_manifest

M = load_manifest("usd")


def test_daycounts():
    cal = M.calendar("us_fed")
    assert year_fraction("ACT/360", dt.date(2026, 1, 1), dt.date(2026, 2, 1)) == 31 / 360
    assert year_fraction("ACT/365F", dt.date(2026, 1, 1), dt.date(2027, 1, 1)) == 1.0
    assert year_fraction("30/360", dt.date(2026, 1, 31), dt.date(2026, 3, 31)) == 60 / 360
    assert abs(year_fraction("BUS/252", dt.date(2026, 10, 1), dt.date(2026, 11, 1), cal) - 21 / 252) < 1e-12


def test_ff_future_is_the_arithmetic_average_over_the_calendar_month():
    """Bloomberg's 9/16/2019 example: Dec 2019 at 11 days of 1.790 and 20 days of 1.658 averages to 1.705."""
    as_of = dt.date(2019, 9, 16)
    c = {x.contract: x for x in listed_contracts(M, "ff_fut", as_of)}["2019-12"]
    assert (c.ref_start, c.ref_end) == (dt.date(2019, 12, 1), dt.date(2020, 1, 1))
    grid = ParcelGrid(as_of, (as_of, dt.date(2019, 12, 12)))        # meeting 11 Dec, effective 12 Dec
    f = AverageRateFuture(M, "ff_fut", c)
    r = f.rate(FlatForwardCurve(grid, [1.790, 1.658]))
    assert abs(r - (11 * 1.790 + 20 * 1.658) / 31) < 1e-12 and abs(r - 1.705) < 5e-4
    assert f.rate_from_quote(98.295) == 100 - 98.295


def test_ff_future_non_publication_days_take_the_previous_published_rate():
    """A step on a Monday effective date: the weekend before it still accrues the old rate."""
    as_of = dt.date(2026, 10, 7)
    c = {x.contract: x for x in listed_contracts(M, "ff_fut", as_of)}["2026-11"]
    eff = dt.date(2026, 11, 9)                                    # Monday
    grid = ParcelGrid(as_of, (as_of, eff))
    r = AverageRateFuture(M, "ff_fut", c).rate(FlatForwardCurve(grid, [4.0, 5.0]))
    assert abs(r - (8 * 4.0 + 22 * 5.0) / 30) < 1e-12               # 1-8 Nov old, 9-30 Nov new


def test_ff_future_past_days_use_fixings():
    as_of = dt.date(2026, 10, 7)
    c = {x.contract: x for x in listed_contracts(M, "ff_fut", as_of)}["2026-10"]
    fix = {dt.date(2026, 10, d): 3.0 for d in range(1, 7)}         # 1-6 Oct fixed at 3.0 (3-4 Oct weekend take the 2nd)
    grid = ParcelGrid(as_of, (as_of, dt.date(2026, 10, 29)), fix)
    r = AverageRateFuture(M, "ff_fut", c).rate(FlatForwardCurve(grid, [4.0, 5.0]))
    assert abs(r - (6 * 3.0 + 22 * 4.0 + 3 * 5.0) / 31) < 1e-12


def test_month_end_adjustment_hook_is_off_by_default_and_lowers_the_average_when_on():
    as_of = dt.date(2026, 10, 7)
    c = {x.contract: x for x in listed_contracts(M, "ff_fut", as_of)}["2026-11"]
    grid = ParcelGrid(as_of, (as_of,))
    base = AverageRateFuture(M, "ff_fut", c).rate(FlatForwardCurve(grid, [4.0]))
    adj = AverageRateFuture(M, "ff_fut", c, 10.0, (dt.date(2026, 11, 30),)).rate(FlatForwardCurve(grid, [4.0]))
    assert abs(base - 4.0) < 1e-12 and abs((base - adj) * 100 - 10.0 / 30) < 1e-9


def test_ois_schedule_and_conventions_match_bloombergs_example():
    """9/13/2018: spot 17 Sep; 1W accrues 17-23 Sep (paid 26 Sep); 1M accrues 17 Sep - 16 Oct (30 days)."""
    as_of = dt.date(2018, 9, 13)
    w = OvernightIndexSwap(M, "ois_effr", "1W", as_of)
    assert w.spot == dt.date(2018, 9, 17) and w.periods == [(dt.date(2018, 9, 17), dt.date(2018, 9, 24))]
    assert w.payments == [dt.date(2018, 9, 26)]
    mth = OvernightIndexSwap(M, "ois_effr", "1M", as_of)
    assert mth.periods == [(dt.date(2018, 9, 17), dt.date(2018, 10, 17))]
    y18 = OvernightIndexSwap(M, "ois_effr", "18M", as_of)
    assert [e for _, e in y18.periods] == [dt.date(2019, 3, 18), dt.date(2020, 3, 17)]     # short front stub


def test_ois_par_rate_on_a_flat_curve_compounds_daily_with_weekends_carried():
    """Fixed 1 + r n/360 = prod(1 + r_i d_i/360): on a flat curve the 1W par rate is slightly above the daily rate."""
    as_of = dt.date(2018, 9, 13)
    grid = ParcelGrid(as_of, (as_of,))
    w = OvernightIndexSwap(M, "ois_effr", "1W", as_of)
    r = 1.918
    par = w.rate(FlatForwardCurve(grid, [r]))
    growth = (1 + r / 100 / 360) ** 4 * (1 + 3 * r / 100 / 360)
    assert abs(par - (growth - 1) * 360 / 7 * 100) < 1e-10
    assert 0 < par - r < 0.001


def test_ois_holiday_inside_the_window_carries_the_previous_rate():
    as_of = dt.date(2018, 9, 13)
    grid = ParcelGrid(as_of, (as_of,))
    mth = OvernightIndexSwap(M, "ois_effr", "1M", as_of)
    rd = mth.bind(grid).rate_days[0]
    assert abs(rd.weight.sum() * 360 - 30) < 1e-9                        # 17 Sep - 16 Oct
    assert sorted(rd.weight * 360)[-2:] == [3.0, 4.0]                    # Columbus Day: Fri 5 Oct carries 4 days
    assert np.isclose(rd.weight.sum(), 30 / 360)
