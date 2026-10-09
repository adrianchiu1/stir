"""End-to-end front end on SYNTHETIC market files (tests/synthetic_market.py, temp dir only):
loader -> inputs -> nodes -> prior -> robust fit -> policy outputs -> quality battery -> exports."""
import datetime as dt
import tempfile
from pathlib import Path

import numpy as np

from stircurve.config.loader import load_config
from stircurve.curves.front_end import build, front_end_meetings
from stircurve.policy.export import store_curve, write_exports
from stircurve.policy.outputs import meeting_table
from stircurve.quality import battery
from tests.synthetic_market import SYNTHETIC_SPREAD, write_synthetic_market

D = dt.date
CFG = load_config("usd")


def _build(as_of, **kw):
    root = Path(tempfile.mkdtemp())
    curve, quotes = write_synthetic_market(root, as_of, **kw)
    return build(as_of, root=root), curve, quotes


def test_front_end_recovers_the_synthetic_curve():
    as_of = D(2024, 6, 12)
    fe, curve, _ = _build(as_of)
    truth = dict(zip(curve.grid.starts, curve.rates))
    got = dict(zip(fe.grid.starts, fe.curve.rates))
    assert max(abs(got[s] - truth[s]) for s in got if s in truth) * 100 < 0.05
    assert fe.fit.dropped == [] and fe.fit.converged
    assert abs(fe.spread.value - SYNTHETIC_SPREAD) < 1e-9 and fe.spread.n_turn_dropped == 3
    assert fe.prior_source[0] == "anchor + spread"
    mt = meeting_table(fe)
    # synthetic path: -25bp at the first three of four meetings (-25, 0, -25, -25), flat after
    assert list(mt["moves"].round(2)[:5]) == [-1.0, -1.0, -2.0, -3.0, -3.0]
    assert np.allclose(mt["step_bp"][:4], [-25.0, 0.0, -25.0, -25.0], atol=0.1)
    assert abs(mt["implied_policy"][0] - (5.375 - 0.25)) < 1e-4
    assert not mt["synthetic"].any() and mt["scheduled"].all()
    res = battery.residual_summary(fe)
    assert (res["max_abs_bp"] < 0.1).all()


def test_drop_list_stale_and_outputs():
    as_of = D(2024, 6, 12)
    fe, _, _ = _build(as_of, bump={("ff_fut", "2025-01"): 12.0, ("ois_effr", "9M"): -8.0},
                      stale={("ff_fut", "2025-03"): 6})
    drops = battery.drop_list(fe)
    dropped = drops[drops["status"] == "dropped"]
    assert set(zip(dropped["instrument"], dropped["contract"])) == {("ff_fut", "2025-01"), ("ois_effr", "9M")}
    assert abs(dropped.set_index("contract").loc["2025-01", "residual_bp"] - 12.0) < 1.0
    assert np.isnan(battery.instrument_table(fe).set_index("contract").loc["2025-01", "leverage"])
    # skipped tenors (not in the synthetic dump) carry a reason
    assert (drops[drops["status"] == "skipped"]["reason"] == "no quote on the as-of date").all()
    flags = battery.input_flags(fe)
    stale = flags[flags["flag"] == "stale"]
    assert list(stale["contract"]) == ["2025-03"] and stale["detail"].iloc[0] == "unchanged 6 observations"
    t = battery.instrument_table(fe)
    row = t[(t["contract"] == "2025-03")].iloc[0]
    assert row["weight"] == CFG["front_end"]["fit"]["stale_multiplier"] and row["stale"]
    rep = battery.report(fe)
    for h in ("## Meetings", "## Residuals", "## Drop list", "## Stale and outside-listing", "## Under-identified"):
        assert h in rep
    out = Path(tempfile.mkdtemp())
    p = write_exports(fe, out)
    assert p == out / "usd" / "effr" / "2024-06-12"
    assert {f.name for f in p.iterdir()} == {"meetings.csv", "parcels.csv", "instruments.csv", "report.md"}
    s = store_curve(fe, Path(tempfile.mkdtemp()))
    assert s.name == "2024-06-12.csv" and s.parent.name == "front_end"


def test_synthetic_meetings_are_flagged_and_unscheduled_need_their_decision_date():
    # 2026-10-07: published meetings run to Dec 2027; the 3y horizon needs synthetic ones
    ms = front_end_meetings(CFG, D(2026, 10, 7), D(2029, 10, 14))
    syn = [m for m in ms if m.synthetic]
    assert syn and min(m.decision_date for m in syn) > D(2027, 12, 31)
    assert all(m.regime == "synthetic" for m in syn)
    # 3 Mar 2020 unscheduled cut (effective 4 Mar): unknown on 2 Mar, in the window on 3 Mar
    before = {m.decision_date for m in front_end_meetings(CFG, D(2020, 3, 2), D(2021, 1, 1))}
    on = {m.decision_date for m in front_end_meetings(CFG, D(2020, 3, 3), D(2021, 1, 1))}
    assert D(2020, 3, 3) not in before and D(2020, 3, 3) in on
    assert D(2020, 3, 15) not in on
    # published implementation dates win (D16): 3 Mar 2020 -> 4 Mar
    m = [m for m in front_end_meetings(CFG, D(2020, 3, 3), D(2021, 1, 1)) if m.decision_date == D(2020, 3, 3)][0]
    assert m.effective_date == D(2020, 3, 4) and not m.scheduled


def test_synthetic_meetings_reach_the_outputs():
    as_of = D(2026, 10, 7)
    fe, _, _ = _build(as_of, steps=(0.25, 0.0, -0.25))
    mt = meeting_table(fe)
    assert mt["synthetic"].any()
    assert "(synthetic)" in " ".join(fe.grid.labels)
    assert np.isfinite(mt["implied_rate"]).all()
