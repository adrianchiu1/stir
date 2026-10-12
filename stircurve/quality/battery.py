"""Quality battery for a fitted front end (M2; D4, D10; AC, PR #4).

Per curve:

* ``instrument_table``: every quote with its model rate, repricing residual in bp
  (quote - model, D10), quote noise, liquidity and staleness weights, final Huber
  weight, leverage, leave-one-out residual, and status: ``used``, ``dropped``
  (robust fit), ``excluded`` (metadata rule: a derived settlement price) or
  ``skipped`` (never entered the inputs, with the reason).
* ``drop_list``: dropped, excluded and skipped rows with reasons.
* ``high_leverage``: used quotes that alone pin a parcel (leverage >= threshold):
  an error in one cannot show as a residual, only as a leave-one-out residual.
* ``input_flags``: stale and outside-listing inputs, missing fixings.
* ``parcel_table``: per parcel, identification share, posterior sigma, fitted
  rate, the replica's rate and the difference; parcels beyond the replica's reach
  are prior-driven (equal-step split, D-C).
* ``replica_table``: what WIRP's bootstrap used, skipped and re-solved.
* ``residual_summary``: count, mean, RMS and max |residual| per instrument and status.
* ``report``: the one-page markdown report for the as-of date.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..curves.front_end import CurveFit, FrontEnd
from ..policy.outputs import basis_table, curve_meeting_rows, stub_table


def instrument_table(fe: FrontEnd, c: CurveFit) -> pd.DataFrame:
    fit = c.fit
    thr = fe.cfg["front_end"]["fit"]["drop_weight"]
    dropped = set(fit.dropped)
    loo_thr = fe.cfg["front_end"]["fit"]["loo_drop_z"]
    rows = []
    for i, q in enumerate(c.used):
        status = "dropped" if i in dropped or i in c.loo_dropped else "used"
        reason = (f"Huber weight {fit.huber_weight[i]:.3f} < {thr}" if i in dropped
                  else f"leave-one-out residual {c.loo_bp[i]:+.2f}bp, over {loo_thr} x its effective noise "
                       f"{c.sigma_bp[i] / np.sqrt(c.weights[i]):.2f}bp (alone pinned a parcel)"
                  if i in c.loo_dropped else "")
        rows.append({"curve": c.name, "instrument": q.instrument, "contract": q.contract, "ticker": q.ticker,
                     "start": q.start, "end": q.end, "quote": q.px, "quote_rate": round(q.rate, 6),
                     "model_rate": round(float(fit.model[i]), 6), "residual_bp": round(float(fit.residual_bp[i]), 3),
                     "loo_residual_bp": round(float(c.loo_bp[i]), 3) if np.isfinite(c.loo_bp[i]) else np.nan,
                     "sigma_bp": c.sigma_bp[i], "open_interest": q.open_interest, "volume": q.volume,
                     "liquidity_weight": round(float(c.liquidity[i]), 4), "stale": q.stale, "stale_run": q.stale_run,
                     "weight": round(float(c.weights[i]), 4), "huber_weight": round(float(fit.huber_weight[i]), 4),
                     "leverage": round(float(fit.leverage[i]), 3) if np.isfinite(fit.leverage[i]) else np.nan,
                     "in_replica": q in c.replica_quotes,
                     "status": status, "reason": reason, "notes": "; ".join(q.notes)})
    for q, why in c.excluded:
        rows.append({"curve": c.name, "instrument": q.instrument, "contract": q.contract, "ticker": q.ticker,
                     "start": q.start, "end": q.end, "quote": q.px, "quote_rate": round(q.rate, 6),
                     "open_interest": q.open_interest, "volume": q.volume, "stale": q.stale, "stale_run": q.stale_run,
                     "status": "excluded", "reason": why, "notes": "; ".join(q.notes)})
    for s in fe.inputs.skipped:
        if s.instrument in c.instruments:
            rows.append({"curve": c.name, "instrument": s.instrument, "contract": s.contract, "ticker": s.ticker,
                         "status": "skipped", "reason": s.reason})
    return pd.DataFrame(rows)


def drop_list(fe: FrontEnd, c: CurveFit, include_horizon: bool = False) -> pd.DataFrame:
    t = instrument_table(fe, c)
    d = t[t["status"].isin(["dropped", "excluded", "skipped"])]
    if not include_horizon:
        d = d[~d["reason"].fillna("").str.startswith("beyond the front")]
    cols = ["curve", "instrument", "contract", "ticker", "status", "reason", "residual_bp"]
    return d.reindex(columns=cols).reset_index(drop=True)


def high_leverage(fe: FrontEnd, c: CurveFit) -> pd.DataFrame:
    thr = fe.cfg["front_end"]["fit"]["leverage_threshold"]
    t = instrument_table(fe, c)
    t = t[(t["status"] == "used") & (t["leverage"] >= thr)]
    return t[["curve", "instrument", "contract", "ticker", "quote_rate", "residual_bp", "loo_residual_bp",
              "leverage"]].reset_index(drop=True)


def input_flags(fe: FrontEnd, c: CurveFit) -> pd.DataFrame:
    t = instrument_table(fe, c)
    stale = t[t["stale"] == True]  # noqa: E712
    listing = t[t["notes"].fillna("").str.contains("listing") | t["reason"].fillna("").str.startswith("loader:")]
    rows = [{"curve": c.name, "flag": "stale", "instrument": r.instrument, "contract": r.contract, "status": r.status,
             "detail": f"unchanged {int(r.stale_run)} observations"} for r in stale.itertuples()]
    rows += [{"curve": c.name, "flag": "outside_listing", "instrument": r.instrument, "contract": r.contract,
              "status": r.status, "detail": r.reason if r.status == "skipped" else r.notes} for r in listing.itertuples()]
    if c.missing_fixings:
        rows.append({"curve": c.name, "flag": "missing_fixings", "instrument": fe.cfg["front_end"]["spread"]["fixing"],
                     "contract": "", "status": "used",
                     "detail": "rate dates with no fixing on file, modelled at the nearest earlier fixing or the "
                     "stub rate: " + ", ".join(d.isoformat() for d in c.missing_fixings)})
    return pd.DataFrame(rows, columns=["curve", "flag", "instrument", "contract", "status", "detail"])


def parcel_table(fe: FrontEnd, c: CurveFit) -> pd.DataFrame:
    thr = fe.cfg["front_end"]["fit"]["identified_threshold"]
    ends = c.grid.ends(c.curve_end)
    rep = c.replica.rates
    return pd.DataFrame({
        "curve": c.name, "parcel": list(c.grid.labels), "start": list(c.grid.starts), "end": ends,
        "identification": np.round(c.fit.identification, 4),
        "under_identified": c.fit.identification < thr,
        "posterior_sigma_bp": np.round(c.fit.posterior_sigma_bp, 3),
        "fitted_rate": np.round(c.curve.rates, 6),
        "step_bp": np.round(np.concatenate([[np.nan], np.diff(c.curve.rates) * 100.0]), 3),
        "replica_rate": np.round(rep, 6),
        "fit_minus_replica_bp": np.round((c.curve.rates - rep) * 100.0, 3),
        "beyond_wirp_reach": np.isnan(rep)})


def replica_table(c: CurveFit) -> pd.DataFrame:
    rows = [{"curve": c.name, "key": k, "quote": q, "status": "used"} for k, q in c.replica.used]
    rows += [{"curve": c.name, "key": k, "quote": np.nan, "status": "skipped: " + why} for k, why in c.replica.skipped]
    return pd.DataFrame(rows, columns=["curve", "key", "quote", "status"])


def residual_summary(fe: FrontEnd, c: CurveFit) -> pd.DataFrame:
    t = instrument_table(fe, c)
    rows = []
    for (ins, status), g in t[t["status"].isin(["used", "dropped"])].groupby(["instrument", "status"]):
        r = g["residual_bp"].astype(float)
        rows.append({"curve": c.name, "instrument": ins, "status": status, "n": len(r), "mean_bp": round(r.mean(), 3),
                     "rms_bp": round(float(np.sqrt((r ** 2).mean())), 3), "max_abs_bp": round(r.abs().max(), 3)})
    return pd.DataFrame(rows)


def _md(df: pd.DataFrame, cols: list[str] | None = None) -> str:
    if df is None or df.empty:
        return "_none_\n"
    d = df[cols] if cols else df
    head = "| " + " | ".join(map(str, d.columns)) + " |\n| " + " | ".join("---" for _ in d.columns) + " |\n"
    body = "".join("| " + " | ".join("" if (isinstance(v, float) and np.isnan(v)) else str(v) for v in row) + " |\n"
                   for row in d.itertuples(index=False))
    return head + body


MEETING_COLS = ["decision_date", "synthetic", "unscheduled", "implied_rate", "imp_rate_delta", "n_moves", "pct_move",
                "replica_rate", "fit_minus_replica_bp", "implied_policy", "cumulative_vs_target_bp", "under_identified",
                "posterior_sigma_bp", "beyond_wirp_reach"]


def report(fe: FrontEnd) -> str:
    sp = fe.spread
    lines = [f"# {fe.ccy.upper()} {fe.family.upper()} front end, {fe.as_of}", "",
             f"Anchor ({sp.anchor}) in effect: {fe.anchor_now}. Policy spread ({sp.estimator}, D7): "
             + (f"{sp.value * 100:.2f}bp (winsorised mean {sp.winsorised_mean * 100:.2f}bp, median {sp.median * 100:.2f}bp; "
                f"{sp.n_obs} fixings, {sp.n_turn_dropped} turn days dropped, window {sp.window[0]}..{sp.window[1]})"
                if sp.value is not None else f"none ({sp.note}); implied policy rates and moves vs target left empty")
             + (" **Loader reported blocking problems in the window (see check_market_data.py).**"
                if fe.inputs.loader_report.blocking else ""), ""]
    for c in fe.curves.values():
        fit = c.fit
        mt = pd.DataFrame(curve_meeting_rows(fe, c))
        lines += [
            f"## Curve `{c.name}` ({', '.join(c.instruments)})", "",
            f"Fit: {len(c.used)} quotes ({len(c.dropped)} dropped, {len(c.excluded)} excluded by metadata), "
            f"{fit.iterations} IRLS iterations ({'converged' if fit.converged else 'NOT CONVERGED'}); {c.grid.n} parcels to "
            f"{c.curve_end}, {sum(m.synthetic for m in c.meetings)} synthetic and {sum(not m.scheduled for m in c.meetings)} "
            f"unscheduled meetings. Current implied O/N rate {c.curve.rates[0]:.4f} (replica {c.replica.rates[0]:.4f}; "
            f"stub prior {c.stub_prior:.4f} from {c.stub_prior_source}). WIRP replica reaches {c.wirp_reach} meetings "
            f"on {len(c.replica.used)} quotes.", "",
            "### Meetings", "", _md(mt, MEETING_COLS),
            "### Residuals (bp, quote - model)", "", _md(residual_summary(fe, c)),
            "### Drop list (dropped by the robust fit, excluded by metadata, skipped)", "", _md(drop_list(fe, c)),
            "### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)", "",
            _md(high_leverage(fe, c)),
            "### Stale and outside-listing inputs", "", _md(input_flags(fe, c)),
            "### Parcels: identification, prior vs fitted vs replica", "",
            _md(parcel_table(fe, c), ["parcel", "start", "identification", "under_identified", "posterior_sigma_bp",
                                      "fitted_rate", "step_bp", "replica_rate", "fit_minus_replica_bp"]),
            "### WIRP replica inputs", "", _md(replica_table(c)),
            "Replica notes: " + ("; ".join(c.replica.notes) if c.replica.notes else "none"), ""]
    lines += ["## FF / OIS basis (bp, fit and replica)", "", _md(basis_table(fe)), "## Stub", "", _md(stub_table(fe))]
    return "\n".join(lines)
