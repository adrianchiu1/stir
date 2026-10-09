"""Quality battery for a fitted front end (M2; D4, D10).

* ``instrument_table``: every input quote with its model rate, repricing residual
  in bp (quote - model, D10), quote noise, liquidity and staleness weights, final
  Huber weight and status: ``used``, ``dropped`` (robust fit, with the residual
  that put it there) or ``skipped`` (never entered the fit, with the reason).
* ``drop_list``: the dropped and skipped rows with reasons.
* ``input_flags``: stale and outside-listing inputs, used or skipped.
* ``identification_table``: per parcel, data share, prior, fitted rate and the
  fitted-minus-prior gap; under-identified parcels take the prior's split (D4).
* ``residual_summary``: count, mean, RMS and max |residual| per instrument family.
* ``report``: the one-page markdown report for the as-of date.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..curves.front_end import FrontEnd
from ..policy.outputs import meeting_table


def instrument_table(fe: FrontEnd) -> pd.DataFrame:
    fit = fe.fit
    dropped = set(fit.dropped)
    rows = []
    for i, q in enumerate(fe.used):
        status = "dropped" if i in dropped else "used"
        reason = (f"Huber weight {fit.huber_weight[i]:.3f} < {fe.cfg['front_end']['fit']['drop_weight']}"
                  if i in dropped else "")
        rows.append({"instrument": q.instrument, "contract": q.contract, "ticker": q.ticker,
                     "start": q.start, "end": q.end, "quote": q.px, "quote_rate": round(q.rate, 6),
                     "model_rate": round(float(fit.model[i]), 6), "residual_bp": round(float(fit.residual_bp[i]), 3),
                     "sigma_bp": fe.sigma_bp[i], "open_interest": q.open_interest, "volume": q.volume,
                     "liquidity_weight": round(float(fe.liquidity[i]), 4), "stale": q.stale, "stale_run": q.stale_run,
                     "weight": round(float(fe.weights[i]), 4), "huber_weight": round(float(fit.huber_weight[i]), 4),
                     "leverage": round(float(fit.leverage[i]), 3),
                     "status": status, "reason": reason, "notes": "; ".join(q.notes)})
    for s in fe.inputs.skipped:
        rows.append({"instrument": s.instrument, "contract": s.contract, "ticker": s.ticker, "status": "skipped",
                     "reason": s.reason})
    return pd.DataFrame(rows)


def drop_list(fe: FrontEnd, include_horizon: bool = False) -> pd.DataFrame:
    t = instrument_table(fe)
    d = t[t["status"].isin(["dropped", "skipped"])]
    if not include_horizon:
        d = d[~d["reason"].str.startswith("beyond the front")]
    return d[["instrument", "contract", "ticker", "status", "reason", "residual_bp"]].reset_index(drop=True)


def high_leverage(fe: FrontEnd, threshold: float = 0.9) -> pd.DataFrame:
    """Used quotes that alone pin a parcel: an error in one cannot show as a residual."""
    t = instrument_table(fe)
    t = t[(t["status"] == "used") & (t["leverage"] >= threshold)]
    return t[["instrument", "contract", "ticker", "quote_rate", "residual_bp", "leverage"]].reset_index(drop=True)


def input_flags(fe: FrontEnd) -> pd.DataFrame:
    t = instrument_table(fe)
    stale = t[t["stale"] == True]  # noqa: E712
    listing = t[t["notes"].fillna("").str.contains("listing") | t["reason"].fillna("").str.startswith("loader:")]
    rows = [{"flag": "stale", "instrument": r.instrument, "contract": r.contract, "status": r.status,
             "detail": f"unchanged {int(r.stale_run)} observations"} for r in stale.itertuples()]
    rows += [{"flag": "outside_listing", "instrument": r.instrument, "contract": r.contract, "status": r.status,
              "detail": r.reason if r.status == "skipped" else r.notes} for r in listing.itertuples()]
    if fe.missing_fixings:
        rows.append({"flag": "missing_fixings", "instrument": fe.cfg["front_end"]["spread"]["fixing"], "contract": "",
                     "status": "used", "detail": "rate dates with no fixing on file, modelled at the nearest earlier "
                     "fixing or the stub rate: " + ", ".join(d.isoformat() for d in fe.missing_fixings)})
    return pd.DataFrame(rows, columns=["flag", "instrument", "contract", "status", "detail"])


def identification_table(fe: FrontEnd) -> pd.DataFrame:
    thr = fe.cfg["front_end"]["fit"]["identified_threshold"]
    ends = fe.grid.ends(fe.curve_end)
    return pd.DataFrame({
        "parcel": list(fe.grid.labels), "start": list(fe.grid.starts), "end": ends,
        "identification": np.round(fe.fit.identification, 4),
        "under_identified": fe.fit.identification < thr,
        "prior_rate": np.round(fe.prior, 6), "prior_source": fe.prior_source,
        "fitted_rate": np.round(fe.curve.rates, 6),
        "fitted_minus_prior_bp": np.round((fe.curve.rates - fe.prior) * 100.0, 3)})


def residual_summary(fe: FrontEnd) -> pd.DataFrame:
    t = instrument_table(fe)
    rows = []
    for (ins, status), g in t[t["status"] != "skipped"].groupby(["instrument", "status"]):
        r = g["residual_bp"].astype(float)
        rows.append({"instrument": ins, "status": status, "n": len(r), "mean_bp": round(r.mean(), 3),
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


def report(fe: FrontEnd) -> str:
    sp = fe.spread
    fit = fe.fit
    mt = meeting_table(fe)
    ident = identification_table(fe)
    under = ident[ident["under_identified"]]
    blocking = fe.inputs.loader_report.blocking
    lines = [
        f"# {fe.ccy.upper()} {fe.cfg['front_end']['family'].upper()} front end, {fe.as_of}",
        "",
        f"Fit: {len(fe.used)} quotes, {len(fit.dropped)} dropped, {fit.iterations} IRLS iterations"
        f" ({'converged' if fit.converged else 'NOT CONVERGED'}); {fe.grid.n} parcels to {fe.curve_end}, "
        f"{sum(m.synthetic for m in fe.meetings)} synthetic and {sum(not m.scheduled for m in fe.meetings)} unscheduled meetings."
        + (" **Loader reported blocking problems in the window (see check_market_data.py).**" if blocking else ""),
        "",
        f"Anchor ({sp.anchor}) in effect: {fe.anchor_now}. Policy spread ({sp.estimator}, D7): "
        + (f"{sp.value * 100:.2f}bp (winsorised mean {sp.winsorised_mean * 100:.2f}bp, median {sp.median * 100:.2f}bp; "
           f"{sp.n_obs} fixings, {sp.n_turn_dropped} turn days dropped, window {sp.window[0]}..{sp.window[1]})"
           if sp.value is not None else f"none ({sp.note}); implied policy rates and moves left empty"),
        "",
        "## Meetings",
        "",
        _md(mt, ["decision_date", "effective_date", "synthetic", "scheduled", "implied_rate", "implied_policy",
                 "step_bp", "cumulative_bp", "moves", "under_identified"]),
        "## Residuals (bp, quote - model)",
        "",
        _md(residual_summary(fe)),
        "## Drop list",
        "",
        _md(drop_list(fe)),
        "High-leverage quotes (>= 0.9: each alone pins a parcel, so an error in it moves the curve "
        "instead of showing as a residual):",
        "",
        _md(high_leverage(fe)),
        "## Stale and outside-listing inputs",
        "",
        _md(input_flags(fe)),
        "## Under-identified parcels: prior vs fitted (D4)",
        "",
        _md(under, ["parcel", "start", "end", "identification", "prior_source", "prior_rate", "fitted_rate",
                    "fitted_minus_prior_bp"]),
    ]
    return "\n".join(lines)
