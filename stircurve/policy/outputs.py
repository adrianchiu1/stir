"""Per-meeting policy outputs from a fitted front end (M2; AC, PR #4).

One row per (curve, meeting) whose effective date is after the as-of date, in
WIRP's definitions (docs/research/wirp) plus ours:

* ``current_implied``: the stub parcel (WIRP's Current Implied O/N Rate, read from
  the instrument, not from the fixing),
* ``implied_rate``: the fitted overnight rate of the parcel the meeting opens
  (WIRP's Post-Meeting Implied Rate),
* ``imp_rate_delta``: implied_rate - current_implied (Imp. Rate Δ),
* ``n_moves``: imp_rate_delta / A.R.M. (#Hikes/Cuts, cumulative),
* ``pct_move``: (implied_rate - previous parcel) / A.R.M. x 100 (%Hike/Cut, marginal),
* ``step_bp``: the same step in bp,
* ``replica_*``: WIRP's sequential bootstrap on the same quotes (NaN beyond its reach),
  and ``fit_minus_replica_bp``,
* ``implied_policy``: implied_rate - policy spread (D7): the implied anchor (target midpoint),
* ``cumulative_vs_target_bp``: implied_policy minus the anchor in effect on the as-of date,
  ``moves_vs_target`` the same in A.R.M. units (the brief's "cumulative change vs the current target"),
* flags: ``synthetic`` (D2), ``unscheduled`` (D11), ``beyond_wirp_reach`` (no instrument WIRP
  would use prices it), ``under_identified`` (the step prior decides it), and the posterior
  sigma of the parcel in bp.

Without a spread (too few fixings) the policy columns are empty.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..curves.front_end import CurveFit, FrontEnd


def curve_meeting_rows(fe: FrontEnd, c: CurveFit) -> list[dict]:
    arm = fe.cfg["front_end"]["move_size"]
    thr = fe.cfg["front_end"]["fit"]["identified_threshold"]
    x, rep = c.curve.rates, c.replica.rates
    spread = fe.spread.value
    cur, rcur = float(x[0]), float(rep[0])
    rows = []
    for k, mt in enumerate(c.meetings, start=1):
        implied, r = float(x[k]), float(rep[k])
        policy = implied - spread if spread is not None else np.nan
        row = {
            "curve": c.name, "decision_date": mt.decision_date, "effective_date": mt.effective_date,
            "scheduled": mt.scheduled, "synthetic": mt.synthetic, "unscheduled": not mt.scheduled,
            "current_implied": round(cur, 6),
            "implied_rate": round(implied, 6), "imp_rate_delta": round(implied - cur, 6),
            "n_moves": round((implied - cur) / arm, 4), "pct_move": round((implied - float(x[k - 1])) / arm * 100.0, 2),
            "step_bp": round((implied - float(x[k - 1])) * 100.0, 3),
            "replica_rate": round(r, 6) if np.isfinite(r) else np.nan,
            "replica_delta": round(r - rcur, 6) if np.isfinite(r) else np.nan,
            "replica_n_moves": round((r - rcur) / arm, 4) if np.isfinite(r) else np.nan,
            "replica_pct_move": (round((r - float(rep[k - 1])) / arm * 100.0, 2)
                                 if np.isfinite(r) and np.isfinite(rep[k - 1]) else np.nan),
            "fit_minus_replica_bp": round((implied - r) * 100.0, 3) if np.isfinite(r) else np.nan,
            "beyond_wirp_reach": not np.isfinite(r),
            "implied_policy": round(policy, 6) if spread is not None else np.nan,
            "cumulative_vs_target_bp": (round((policy - fe.anchor_now) * 100.0, 3)
                                        if spread is not None and fe.anchor_now is not None else np.nan),
            "moves_vs_target": (round((policy - fe.anchor_now) / arm, 4)
                                if spread is not None and fe.anchor_now is not None else np.nan),
            "identification": round(float(c.fit.identification[k]), 4),
            "under_identified": bool(c.fit.identification[k] < thr),
            "posterior_sigma_bp": round(float(c.fit.posterior_sigma_bp[k]), 3),
        }
        rows.append(row)
    return rows


def meeting_table(fe: FrontEnd) -> pd.DataFrame:
    rows = []
    for c in fe.curves.values():
        rows += curve_meeting_rows(fe, c)
    return pd.DataFrame(rows)


def stub_table(fe: FrontEnd) -> pd.DataFrame:
    """The parcel from the as-of date to the first effective date, per curve."""
    sp = fe.spread
    return pd.DataFrame([{
        "curve": c.name, "as_of": fe.as_of, "current_implied": round(float(c.curve.rates[0]), 6),
        "replica_current_implied": round(float(c.replica.rates[0]), 6),
        "stub_prior": round(c.stub_prior, 6), "stub_prior_source": c.stub_prior_source,
        "anchor": fe.anchor_now, "spread": sp.value, "spread_median": sp.median,
        "spread_winsorised_mean": sp.winsorised_mean, "spread_obs": sp.n_obs, "spread_estimator": sp.estimator,
        "spread_note": sp.note, "wirp_reach_meetings": c.wirp_reach}
        for c in fe.curves.values()])


def basis_table(fe: FrontEnd) -> pd.DataFrame:
    """FF-implied minus OIS-implied post-meeting rate per meeting (fit and replica), bp: the diagnostic
    D5 asks for; the two are separate instruments (AC, PR #4) and nothing reconciles them."""
    names = list(fe.curves)
    if len(names) < 2:
        return pd.DataFrame()
    a, b = fe.curves[names[0]], fe.curves[names[1]]
    by_b = {m.effective_date: k for k, m in enumerate(b.meetings, start=1)}
    rows = [{"decision_date": None, "effective_date": None, "parcel": "stub",
             f"{a.name}_fit": a.curve.rates[0], f"{b.name}_fit": b.curve.rates[0],
             "basis_fit_bp": round((a.curve.rates[0] - b.curve.rates[0]) * 100.0, 3),
             "basis_replica_bp": round((a.replica.rates[0] - b.replica.rates[0]) * 100.0, 3)}]
    for k, mt in enumerate(a.meetings, start=1):
        j = by_b.get(mt.effective_date)
        if j is None:
            continue
        rb = (a.replica.rates[k] - b.replica.rates[j]) * 100.0
        rows.append({"decision_date": mt.decision_date, "effective_date": mt.effective_date, "parcel": k,
                     f"{a.name}_fit": round(float(a.curve.rates[k]), 6), f"{b.name}_fit": round(float(b.curve.rates[j]), 6),
                     "basis_fit_bp": round(float((a.curve.rates[k] - b.curve.rates[j]) * 100.0), 3),
                     "basis_replica_bp": round(float(rb), 3) if np.isfinite(rb) else np.nan})
    return pd.DataFrame(rows)
