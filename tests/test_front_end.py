"""End-to-end front end on SYNTHETIC market files (tests/synthetic_market.py; nothing under data/)."""
import datetime as dt
import tempfile
from pathlib import Path

import numpy as np

from stircurve.curves.front_end import build, market_inputs
from stircurve.config.loader import load_config
from stircurve.marketdata.manifest import load_manifest
from stircurve.policy.export import write_exports
from stircurve.policy.outputs import basis_table, meeting_table
from stircurve.quality import battery
from tests.synthetic_market import write_synthetic_market

AS_OF = dt.date(2026, 10, 7)


def _build(root: Path, **kw):
    curve, quotes = write_synthetic_market(root, AS_OF, **kw)
    m, cfg = load_manifest("usd"), load_config("usd")
    inputs = market_inputs(m, cfg, AS_OF, root)
    return curve, quotes, build(AS_OF, "usd", m, cfg, inputs, root=root)


def test_both_curves_recover_the_true_steps_and_the_replica_agrees():
    with tempfile.TemporaryDirectory() as tmp:
        truth, quotes, fe = _build(Path(tmp))
        assert set(fe.curves) == {"effr_fut", "effr_ois"}
        for c in fe.curves.values():
            n = c.wirp_reach
            assert n >= 8, c.name
            assert np.max(np.abs(c.curve.rates[: n + 1] - truth.rates[: n + 1])) * 100 < 0.1, c.name
            assert np.max(np.abs(c.replica.rates[: n + 1] - truth.rates[: n + 1])) * 100 < 0.05, c.name
            assert not c.dropped and c.fit.converged
            assert np.max(np.abs(c.fit.residual_bp)) < 0.25
        # beyond every instrument the step prior continues the last level (flat): still the truth here (steps are 0)
        c = fe.curves["effr_ois"]
        assert np.max(np.abs(c.curve.rates - truth.rates[: c.grid.n])) * 100 < 0.5
        mt = meeting_table(fe)
        assert set(mt["curve"]) == {"effr_fut", "effr_ois"} and (mt["synthetic"].sum() > 0)
        assert np.allclose(mt["n_moves"] * 0.25, mt["imp_rate_delta"], atol=5e-5)   # n_moves is rounded to 4 places
        assert fe.spread.value is not None and abs(fe.spread.value - 0.08) < 1e-6      # month-ends dropped (D7)
        assert abs(mt["cumulative_vs_target_bp"].iloc[0] - (-25.0)) < 0.1              # first synthetic step: -25bp
        b = basis_table(fe)
        assert np.nanmax(np.abs(b["basis_fit_bp"])) < 0.5


def test_derived_far_contracts_are_excluded_and_a_bad_quote_is_dropped_with_reasons():
    with tempfile.TemporaryDirectory() as tmp:
        truth, quotes, fe = _build(Path(tmp), dead_from=14, bump={("ff_fut", "2027-02"): 6.0})
        c = fe.curves["effr_fut"]
        reasons = {q.contract: why for q, why in c.excluded}
        assert len(reasons) >= 10 and all("derived settlement price" in w for w in reasons.values())
        assert "2027-02" not in reasons
        dropped = [c.used[i].contract for i in c.dropped]
        assert dropped == ["2027-02"], dropped
        assert np.max(np.abs(c.curve.rates[: c.wirp_reach + 1] - truth.rates[: c.wirp_reach + 1])) * 100 < 0.1
        t = battery.instrument_table(fe, c)
        assert set(t["status"]) >= {"used", "dropped", "excluded"}
        dl = battery.drop_list(fe, c)
        assert "2027-02" in set(dl["contract"]) and (dl["status"] == "excluded").sum() >= 10
        # the replica is offered live contracts only, so a dead strip cannot reach beyond them
        assert c.wirp_reach <= 14


def test_stale_quotes_are_flagged_and_down_weighted():
    with tempfile.TemporaryDirectory() as tmp:
        truth, quotes, fe = _build(Path(tmp), stale={("ois_effr", "6M"): 9})
        c = fe.curves["effr_ois"]
        q = [x for x in c.used if x.contract == "6M"][0]
        assert q.stale and q.stale_run >= 5
        i = c.used.index(q)
        assert abs(c.weights[i] - 0.1) < 1e-9
        flags = battery.input_flags(fe, c)
        assert "stale" in set(flags["flag"])


def test_exports_and_report():
    with tempfile.TemporaryDirectory() as tmp:
        truth, quotes, fe = _build(Path(tmp))
        out = write_exports(fe, Path(tmp) / "exports")
        names = {p.name for p in out.iterdir()}
        assert names == {"meetings.csv", "parcels.csv", "instruments.csv", "basis.csv", "report.md"}
        rep = (out / "report.md").read_text(encoding="utf-8")
        assert "## Curve `effr_fut`" in rep and "## Curve `effr_ois`" in rep and "FF / OIS basis" in rep


def test_superseded_meeting_is_a_node_only_before_its_supersession():
    from stircurve.curves.nodes import meeting_nodes
    cfg = load_config("usd")
    before = meeting_nodes(cfg, dt.date(2020, 3, 3), dt.date(2020, 12, 31))
    after = meeting_nodes(cfg, dt.date(2020, 3, 16), dt.date(2020, 12, 31))
    assert dt.date(2020, 3, 18) in {m.decision_date for m in before}
    assert dt.date(2020, 3, 4) in {m.effective_date for m in before}           # the 3 Mar cut: a known step from its decision date
    assert dt.date(2020, 3, 18) not in {m.decision_date for m in after}
    assert dt.date(2020, 3, 16) not in {m.effective_date for m in after}         # effective on the as-of date: in the stub
    # before 3 Mar the unscheduled cut is unknown (no look-ahead)
    earlier = meeting_nodes(cfg, dt.date(2020, 3, 2), dt.date(2020, 12, 31))
    assert dt.date(2020, 3, 4) not in {m.effective_date for m in earlier}
