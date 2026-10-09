"""M2 instrument models and the flat-forward curve on hand-checkable cases.

Rates are made-up round numbers (no market data); calendars and conventions
are the committed ones.
"""
import datetime as dt

import numpy as np

from stircurve.curves.flat_forward import FlatForwardCurve, ParcelGrid
from stircurve.instruments import AverageRateFuture, OvernightIndexSwap, year_fraction
from stircurve.marketdata.contracts import listed_contracts
from stircurve.marketdata.manifest import load_manifest

M = load_manifest("usd")
D = dt.date
FED = M.calendar("us_fed")


def _contract(name, as_of, contract):
    return {c.contract: c for c in listed_contracts(M, name, as_of)}[contract]


def test_daycounts():
    assert year_fraction("ACT/360", D(2024, 1, 1), D(2024, 3, 1)) == 60 / 360
    assert year_fraction("ACT/365F", D(2024, 1, 1), D(2025, 1, 1)) == 366 / 365
    assert year_fraction("30/360", D(2024, 1, 31), D(2024, 3, 31)) == 60 / 360
    # BUS/252 counts business days of the calendar: Mon 1 Jul - Mon 8 Jul 2024 spans the 4 Jul holiday
    assert year_fraction("BUS/252", D(2024, 7, 1), D(2024, 7, 8), FED) == 4 / 252


def test_ff_average_with_fixings_and_a_mid_month_step():
    """Oct 2026: 1-6 Oct fixed at 3.88 (past rate dates), 7-28 Oct at the stub 3.88, 29-31 Oct at 3.63."""
    as_of = D(2026, 10, 7)
    grid = ParcelGrid(as_of, (as_of, D(2026, 10, 29)), {D(2026, 10, d): 3.88 for d in (1, 2, 5, 6)})
    f = AverageRateFuture(M, "ff_fut", _contract("ff_fut", as_of, "2026-10"))
    got = f.rate(FlatForwardCurve(grid, [3.88, 3.63]))
    assert abs(got - (28 * 3.88 + 3 * 3.63) / 31) < 1e-12
    assert f.rate_from_quote(96.115) == 100 - 96.115


def test_ff_non_publication_days_take_the_previous_published_rate():
    """Nov 2025 starts on a Saturday: 1-2 Nov take Fri 31 Oct's rate (the old parcel);
    Veterans Day and Thanksgiving take the day before (same parcel)."""
    as_of = D(2025, 10, 15)
    grid = ParcelGrid(as_of, (as_of, D(2025, 11, 3)))
    f = AverageRateFuture(M, "ff_fut", _contract("ff_fut", as_of, "2025-11"))
    assert abs(f.rate(FlatForwardCurve(grid, [4.0, 3.0])) - (2 * 4.0 + 28 * 3.0) / 30) < 1e-12
    # past fixings: a weekend before the as-of date takes the Friday fixing
    as_of = D(2025, 11, 4)
    grid = ParcelGrid(as_of, (as_of,), {D(2025, 10, 31): 4.10, D(2025, 11, 3): 3.90})
    got = f.rate(FlatForwardCurve(grid, [3.80]))
    assert abs(got - (2 * 4.10 + 1 * 3.90 + 27 * 3.80) / 30) < 1e-12


def test_compounded_future_matches_daily_compounding():
    """SR3 Jun 2024 (19 Jun - 18 Sep 2024) on a flat 5%: CME's compounding over us_sofr days."""
    as_of = D(2024, 5, 1)
    c = _contract("sofr3m_fut", as_of, "2024-06")
    f = AverageRateFuture(M, "sofr3m_fut", c)
    sofr = M.calendar("us_sofr")
    g, d = 1.0, c.ref_start
    while d < c.ref_end:
        nxt = min(sofr.next_business_day(d), c.ref_end)
        g *= 1 + 0.05 * (nxt - d).days / 360
        d = nxt
    want = (g - 1) * 360 / (c.ref_end - c.ref_start).days * 100
    assert abs(f.rate(FlatForwardCurve(ParcelGrid(as_of, (as_of,)), [5.0])) - want) < 1e-12


def test_ois_schedule_from_the_manifest():
    as_of = D(2026, 10, 7)
    s = OvernightIndexSwap(M, "ois_effr", "18M", as_of)
    assert s.spot == D(2026, 10, 9)                                  # two us_fed business days
    assert s.periods == [(D(2026, 10, 9), D(2027, 4, 9)), (D(2027, 4, 9), D(2028, 4, 10))]   # short front stub
    assert s.payments == [D(2027, 4, 13), D(2028, 4, 12)]            # +2 us_fed business days
    one = OvernightIndexSwap(M, "ois_effr", "1Y", as_of)
    assert one.periods == [(D(2026, 10, 9), D(2027, 10, 12))]        # 9 Oct 2027 Sat, 11 Oct Columbus Day
    assert OvernightIndexSwap(M, "ois_effr", "1W", as_of).periods == [(D(2026, 10, 9), D(2026, 10, 16))]


def test_ois_par_rate_by_hand():
    """1Y on a flat 4%: (G - 1) / (days/360). 2Y across a step: explicit discounting."""
    as_of = D(2026, 10, 7)
    one = OvernightIndexSwap(M, "ois_effr", "1Y", as_of)
    (s, e), = one.periods
    g, d = 1.0, s
    while d < e:
        nxt = FED.next_business_day(d)
        g *= 1 + 0.04 * (nxt - d).days / 360
        d = nxt
    flat = FlatForwardCurve(ParcelGrid(as_of, (as_of,)), [4.0])
    assert abs(one.rate(flat) - (g - 1) / ((e - s).days / 360) * 100) < 1e-12

    step = D(2027, 3, 18)
    curve = FlatForwardCurve(ParcelGrid(as_of, (as_of, step)), [4.0, 3.0])
    two = OvernightIndexSwap(M, "ois_effr", "2Y", as_of)

    def growth(a, b):
        out, d = 1.0, a
        while d < b:
            nxt = FED.next_business_day(d)
            out *= 1 + (0.04 if d < step else 0.03) * (nxt - d).days / 360
            d = nxt
        return out
    num = sum((growth(a, b) - 1) / growth(as_of, p) for (a, b), p in zip(two.periods, two.payments))
    den = sum((b - a).days / 360 / growth(as_of, p) for (a, b), p in zip(two.periods, two.payments))
    assert abs(two.rate(curve) - num / den * 100) < 1e-12


def test_flat_forwards_across_effective_dates():
    """Wed 12 Jun 2024 as-of, cut effective Thu 13 Jun: weekend and Juneteenth (us_fed holiday)
    take the previous business day's rate."""
    as_of = D(2024, 6, 12)
    curve = FlatForwardCurve(ParcelGrid(as_of, (as_of, D(2024, 6, 13)), {D(2024, 6, 11): 5.33}), [5.33, 5.08])
    assert curve.rate_on(D(2024, 6, 11), FED) == 5.33               # past: the fixing
    assert curve.rate_on(D(2024, 6, 12), FED) == 5.33
    assert curve.rate_on(D(2024, 6, 13), FED) == 5.08
    assert curve.rate_on(D(2024, 6, 16), FED) == 5.08               # Sunday
    want = 1 / ((1 + .0533 / 360) * (1 + .0508 / 360) * (1 + .0508 * 3 / 360) * (1 + .0508 / 360)
                * (1 + .0508 * 2 / 360) * (1 + .0508 / 360))
    assert abs(curve.discount(D(2024, 6, 21), FED, "ACT/360") - want) < 1e-15
    # the parcel containing a day; days before the as-of date are not on the curve
    assert curve.grid.parcel_of(D(2024, 6, 12)) == 0 and curve.grid.parcel_of(D(2030, 1, 1)) == 1
    try:
        curve.grid.parcel_of(D(2024, 6, 11))
        raise AssertionError("expected ValueError")
    except ValueError:
        pass


def test_missing_past_fixing_is_reported():
    as_of = D(2024, 6, 12)
    grid = ParcelGrid(as_of, (as_of,), {D(2024, 5, 31): 5.33})
    f = AverageRateFuture(M, "ff_fut", _contract("ff_fut", as_of, "2024-06"))
    b = f.bind(grid)
    # 3-11 Jun have no fixing: the last one within a week stands in, then the stub
    assert b.missing_fixings[0] == D(2024, 6, 3)
    v = b.value(np.array([5.0]))
    assert 5.0 < v < 5.33
