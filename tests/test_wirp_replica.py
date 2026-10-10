"""The replica of WIRP's two models on Bloomberg's own worked examples (docs/research/wirp)."""
import datetime as dt

import numpy as np

from stircurve.curves.flat_forward import ParcelGrid
from stircurve.curves.wirp_replica import sequential_bootstrap, wirp_outputs
from stircurve.instruments import AverageRateFuture, OvernightIndexSwap
from stircurve.marketdata.contracts import listed_contracts
from stircurve.marketdata.manifest import load_manifest

M = load_manifest("usd")


def _ff(as_of, contract):
    c = {x.contract: x for x in listed_contracts(M, "ff_fut", as_of)}[contract]
    return c


def test_futures_model_reproduces_bloombergs_december_2019_example():
    """Nov 2019 (no meeting) at 1.790 carried into Dec 2019 (98.295): post-meeting rate ~1.658."""
    as_of = dt.date(2019, 9, 16)
    grid = ParcelGrid(as_of, (as_of, dt.date(2019, 9, 19), dt.date(2019, 10, 31), dt.date(2019, 12, 12)))
    ins = [("FF 2019-11", AverageRateFuture(M, "ff_fut", _ff(as_of, "2019-11")).bind(grid), 1.790, dt.date(2019, 12, 1)),
           ("FF 2019-12", AverageRateFuture(M, "ff_fut", _ff(as_of, "2019-12")).bind(grid), 100 - 98.295, dt.date(2020, 1, 1))]
    r = sequential_bootstrap("futures", grid, ins)
    assert abs(r.rates[2] - 1.790) < 1e-9 and abs(r.rates[3] - 1.658) < 5e-4
    assert np.isnan(r.rates[1])                                   # no contract prices the post-September parcel
    assert r.solved_by == {2: "FF 2019-11", 3: "FF 2019-12"}


def test_futures_model_solves_the_stub_and_first_step_jointly():
    """Sep 2019 has two unknowns (stub, post-18 Sep); October has one day of the post-30 Oct rate, so the
    system closes only with November (no meeting): the three are solved together."""
    as_of = dt.date(2019, 9, 16)
    fix = {dt.date(2019, 9, d): 2.13 for d in range(1, 16)}
    grid = ParcelGrid(as_of, (as_of, dt.date(2019, 9, 19), dt.date(2019, 10, 31)), fix)
    truth = np.array([2.16, 1.90, 1.65])
    ins = []
    for con, end in (("2019-09", dt.date(2019, 10, 1)), ("2019-10", dt.date(2019, 11, 1)), ("2019-11", dt.date(2019, 12, 1))):
        b = AverageRateFuture(M, "ff_fut", _ff(as_of, con)).bind(grid)
        ins.append((f"FF {con}", b, b.value(truth), end))
    r = sequential_bootstrap("futures", grid, ins)
    assert np.allclose(r.rates, truth, atol=1e-8)
    assert r.solved_by[0] == "FF 2019-09 + FF 2019-10 + FF 2019-11"


def test_non_meeting_month_overrides_the_level_carried_from_the_previous_contract():
    """Oct and Nov 2019 both price the same parcel: November (the more direct quote) wins."""
    as_of = dt.date(2019, 9, 16)
    grid = ParcelGrid(as_of, (as_of, dt.date(2019, 12, 12)))
    octo = AverageRateFuture(M, "ff_fut", _ff(as_of, "2019-10")).bind(grid)
    nov = AverageRateFuture(M, "ff_fut", _ff(as_of, "2019-11")).bind(grid)
    ins = [("FF 2019-10", octo, 1.80, dt.date(2019, 11, 1)), ("FF 2019-11", nov, 1.79, dt.date(2019, 12, 1))]
    r = sequential_bootstrap("futures", grid, ins)
    assert abs(r.rates[0] - 1.79) < 1e-9 and r.solved_by[0] == "FF 2019-11" and any("re-solved" in n for n in r.notes)


def test_ois_model_reproduces_bloombergs_september_2018_example():
    """1W at 1.9195 -> ~1.918 before the 26 Sep meeting; 1M at 2.0830 -> ~2.165 after (Bloomberg rounds its
    intermediate values; the exact solution of its equations is 1.9192 and 2.1624)."""
    as_of = dt.date(2018, 9, 13)
    grid = ParcelGrid(as_of, (as_of, dt.date(2018, 9, 27)))
    ins = [("OIS 1W", OvernightIndexSwap(M, "ois_effr", "1W", as_of).bind(grid), 1.9195, dt.date(2018, 9, 24)),
           ("OIS 1M", OvernightIndexSwap(M, "ois_effr", "1M", as_of).bind(grid), 2.0830, dt.date(2018, 10, 17))]
    r = sequential_bootstrap("ois", grid, ins)
    assert abs(r.rates[0] - 1.918) < 2e-3 and abs(r.rates[1] - 2.165) < 3e-3
    assert abs(r.rates[0] - 1.91924) < 1e-4 and abs(r.rates[1] - 2.16236) < 1e-4
    out = wirp_outputs(r, 0.25)
    assert abs(out[0]["n_moves"] - (r.rates[1] - r.rates[0]) / 0.25) < 1e-12 and abs(out[0]["pct_move"] - 97.2) < 0.2


def test_ois_tenor_that_only_discounts_into_a_parcel_does_not_price_it():
    """A 2M OIS paying two days into the next parcel re-solves the previous parcel (WIRP works through the
    monthly tenors) rather than pinning the next one from two days of discounting."""
    as_of = dt.date(2026, 10, 7)
    grid = ParcelGrid(as_of, (as_of, dt.date(2026, 10, 29), dt.date(2026, 12, 10)))
    truth = np.array([3.88, 3.93, 4.13])
    ins = []
    for t, end in (("1W", 1), ("1M", 2), ("2M", 3), ("3M", 4)):
        s = OvernightIndexSwap(M, "ois_effr", t, as_of)
        b = s.bind(grid)
        ins.append((f"OIS {t}", b, b.value(truth), s.end))
    r = sequential_bootstrap("ois", grid, ins)
    assert np.allclose(r.rates, truth, atol=1e-7)
    assert r.solved_by[1] == "OIS 2M" and r.solved_by[2] == "OIS 3M"
