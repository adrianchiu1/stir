"""Robust IRLS (Huber) and the D4 prior on constructed problems (no market data)."""
import datetime as dt

import numpy as np

from stircurve.curves import robust
from stircurve.curves.flat_forward import ParcelGrid
from stircurve.instruments import AverageRateFuture
from stircurve.marketdata.contracts import listed_contracts
from stircurve.marketdata.manifest import load_manifest

M = load_manifest("usd")
D = dt.date


def _ff_obs(as_of, grid, months, truth, bump=None, weight=None):
    cons = {c.contract: c for c in listed_contracts(M, "ff_fut", as_of)}
    obs = []
    for con in months:
        b = AverageRateFuture(M, "ff_fut", cons[con]).bind(grid)
        tgt = b.value(truth) + (bump or {}).get(con, 0.0) / 100
        obs.append(robust.Observation(con, b.value, tgt, 0.5, (weight or {}).get(con, 1.0)))
    return obs


def test_irls_recovers_the_curve_and_drops_the_outlier():
    """Over-identified: 3 parcels, 8 monthly contracts (Aug, Sep, Oct all inside one parcel);
    the Sep quote is 15bp off."""
    as_of = D(2024, 6, 12)
    grid = ParcelGrid(as_of, (as_of, D(2024, 8, 1), D(2024, 11, 8)))
    truth = np.array([5.33, 5.08, 4.83])
    months = [f"2024-{m:02d}" for m in range(6, 13)] + ["2025-01"]
    obs = _ff_obs(as_of, grid, months, truth, bump={"2024-09": 15.0})
    res = robust.fit(obs, prior=np.full(3, 5.0), prior_sigma_bp=10.0)
    assert [obs[i].key for i in res.dropped] == ["2024-09"]
    assert np.abs(res.x - truth).max() * 100 < 0.1        # prior 5.0 is 33bp off: ridge bias ~0.04bp
    assert abs(res.residual_bp[months.index("2024-09")] - 15.0) < 0.05
    assert res.converged and (res.identification > 0.999).all()
    # without the outlier nothing is dropped and the fit is exact
    clean = robust.fit(_ff_obs(as_of, grid, months, truth), prior=np.full(3, 5.0), prior_sigma_bp=10.0)
    assert clean.dropped == [] and np.abs(clean.x - truth).max() * 100 < 0.1
    # a prior at the truth: no bias at all
    exact = robust.fit(_ff_obs(as_of, grid, months, truth), prior=truth, prior_sigma_bp=10.0)
    assert np.abs(exact.x - truth).max() * 100 < 1e-6


def test_a_quote_that_alone_pins_a_parcel_has_full_leverage():
    """The Oct contract is the only one inside the 19 Sep - 7 Nov parcel: a 15bp error there
    moves the parcel instead of standing out (no residual-based method can see it), so the
    robust fit blames its neighbours. The leverage column shows it (D4 drop-list review)."""
    as_of = D(2024, 6, 12)
    grid = ParcelGrid(as_of, (as_of, D(2024, 8, 1), D(2024, 9, 19), D(2024, 11, 8)))
    truth = np.array([5.33, 5.08, 4.83, 4.58])
    months = [f"2024-{m:02d}" for m in range(6, 13)] + ["2025-01", "2025-02"]
    obs = _ff_obs(as_of, grid, months, truth, bump={"2024-10": 15.0})
    res = robust.fit(obs, prior=np.full(4, 5.0), prior_sigma_bp=10.0)
    oct_ = months.index("2024-10")
    assert oct_ not in res.dropped and abs(res.residual_bp[oct_]) < 0.5
    assert res.leverage[oct_] > 0.9 > max(res.leverage[i] for i in range(len(obs)) if months[i] in ("2024-06", "2024-12"))


def test_liquidity_weights_decide_between_conflicting_quotes():
    """Two quotes on the same window 2bp apart: the liquid one wins in proportion to its weight."""
    as_of = D(2024, 6, 12)
    grid = ParcelGrid(as_of, (as_of,))
    cons = {c.contract: c for c in listed_contracts(M, "ff_fut", as_of)}
    b = AverageRateFuture(M, "ff_fut", cons["2024-07"]).bind(grid)
    obs = [robust.Observation("liquid", b.value, 5.30, 0.5, 1.0), robust.Observation("thin", b.value, 5.32, 0.5, 0.25)]
    res = robust.fit(obs, prior=np.array([5.0]), prior_sigma_bp=1e6, huber_k=100.0)
    assert abs(res.x[0] - (5.30 * 1.0 + 5.32 * 0.25) / 1.25) < 1e-8


def test_prior_splits_an_under_identified_pair():
    """The Sep 2024 contract covers two parcels (split on 17 Sep): the data pin only their
    average; the split follows the prior's (the OIS family's, D4)."""
    as_of = D(2024, 6, 12)
    grid = ParcelGrid(as_of, (as_of, D(2024, 9, 3), D(2024, 9, 17), D(2024, 10, 1)))
    truth = np.array([5.33, 5.20, 5.00, 4.90])
    obs = _ff_obs(as_of, grid, ["2024-06", "2024-07", "2024-08", "2024-09", "2024-10"], truth)
    prior = np.array([5.33, 5.30, 5.10, 4.90])          # prior split: 20bp between the pair
    res = robust.fit(obs, prior=prior, prior_sigma_bp=10.0)
    ident = res.identification
    assert ident[0] > 0.999 and ident[3] > 0.999
    assert abs(ident[1] - 0.5) < 1e-6 and abs(ident[2] - 0.5) < 1e-6
    # the September average is matched...
    assert abs(obs[3].value(res.x) - obs[3].target) * 100 < 0.1
    # ...and the pair keeps the prior's gap (the data say nothing about it)
    assert abs((res.x[1] - res.x[2]) - (prior[1] - prior[2])) * 100 < 1e-6
    # the identified neighbours stay at the data (the prior is at the truth there)
    assert abs(res.x[0] - truth[0]) * 100 < 0.01 and abs(res.x[3] - truth[3]) * 100 < 0.01


def test_huber_weights():
    w = robust.huber_weights(np.array([0.0, 1.0, -2.69, 13.45]), 1.345)
    assert list(np.round(w, 3)) == [1.0, 1.0, 0.5, 0.1]
