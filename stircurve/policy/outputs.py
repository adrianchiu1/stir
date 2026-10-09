"""Per-meeting policy outputs from a fitted front end (M2).

For each meeting whose effective date is after the as-of date:

* ``implied_rate``: the fitted overnight (EFFR) rate of the parcel the meeting opens,
* ``implied_policy``: that minus the policy spread (D7): the implied anchor (target midpoint),
* ``step_bp``: change vs the previous meeting's parcel (the first meeting: vs the stub),
* ``cumulative_bp``: implied anchor minus the anchor in effect on the as-of date,
* ``moves``: cumulative change in units of ``front_end.move_size`` (25bp moves priced),
* ``synthetic`` / ``unscheduled`` flags (D2, D11), the parcel's identification share and
  the prior it was pulled towards.

Without a spread (too few fixings) the implied anchor and the moves are left empty and
the cumulative change is measured on the EFFR level against the stub.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..curves.front_end import FrontEnd


def meeting_table(fe: FrontEnd) -> pd.DataFrame:
    move = fe.cfg["front_end"]["move_size"]
    thr = fe.cfg["front_end"]["fit"]["identified_threshold"]
    x, prior, ident = fe.curve.rates, fe.prior, fe.fit.identification
    spread = fe.spread.value
    rows = []
    for k, mt in enumerate(fe.meetings, start=1):
        implied = float(x[k])
        policy = implied - spread if spread is not None else np.nan
        if spread is not None and fe.anchor_now is not None:
            cum = (policy - fe.anchor_now) * 100.0
        else:
            cum = (implied - float(x[0])) * 100.0
        rows.append({
            "decision_date": mt.decision_date, "effective_date": mt.effective_date,
            "scheduled": mt.scheduled, "synthetic": mt.synthetic,
            "implied_rate": round(implied, 6), "implied_policy": round(policy, 6) if spread is not None else np.nan,
            "step_bp": round((implied - float(x[k - 1])) * 100.0, 3),
            "cumulative_bp": round(cum, 3),
            "moves": round(cum / (move * 100.0), 3),
            "identification": round(float(ident[k]), 4), "under_identified": bool(ident[k] < thr),
            "prior_rate": round(float(prior[k]), 6),
        })
    return pd.DataFrame(rows)


def stub_row(fe: FrontEnd) -> dict:
    """The parcel from the as-of date to the first effective date."""
    return {"as_of": fe.as_of, "stub_rate": float(fe.curve.rates[0]), "anchor": fe.anchor_now,
            "spread": fe.spread.value, "spread_median": fe.spread.median,
            "spread_winsorised_mean": fe.spread.winsorised_mean, "spread_obs": fe.spread.n_obs,
            "spread_estimator": fe.spread.estimator, "spread_note": fe.spread.note}
