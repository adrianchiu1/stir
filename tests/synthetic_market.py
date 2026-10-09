"""SYNTHETIC market data for the M2 tests. Not Bloomberg data.

Writes wide CSVs in the dump's layout (``<root>/usd/<YYYY>/<group>.csv``, columns
``<ticker>|<field>``) into a temporary directory, priced exactly from a known
flat-forward curve on the real Fed meeting grid. Nothing here is written under
``data/``; every test calls ``write_synthetic_market`` with a temporary root.
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import numpy as np
import pandas as pd

from stircurve.config.loader import load_config
from stircurve.curves.flat_forward import FlatForwardCurve
from stircurve.curves.nodes import build_grid, meeting_nodes
from stircurve.instruments import AverageRateFuture, OvernightIndexSwap
from stircurve.marketdata.contracts import listed_contracts
from stircurve.marketdata.manifest import load_manifest
from stircurve.refdata.calendars import add_months
from stircurve.refdata.maintenance import load_policy_rates, rate_in_effect

SYNTHETIC_SPREAD = 0.08          # percent: EFFR = target midpoint + 8bp on non-turn days
TURN_BUMP = -0.05                # percent added on month-end days (dropped by the spread estimator)


def true_curve(as_of: dt.date, through: dt.date, start_rate: float, steps: list[float],
               fixings: dict | None = None) -> FlatForwardCurve:
    """Stub at ``start_rate``; meeting k moves by ``steps[k]`` (0 beyond the list)."""
    cfg = load_config("usd")
    ms = meeting_nodes(cfg, as_of, through)
    grid = build_grid(as_of, ms, fixings or {})
    x = start_rate + np.concatenate([[0.0], np.cumsum([steps[i] if i < len(steps) else 0.0 for i in range(len(ms))])])
    return FlatForwardCurve(grid, x)


def write_synthetic_market(root: Path, as_of: dt.date, *, steps=(-0.25, 0.0, -0.25, -0.25), history_bd: int = 90,
                           bump: dict | None = None, stale: dict | None = None, oi: float = 100000.0,
                           dead_from: int | None = None,
                           ois_tenors=("1W", "2W", "3W", "1M", "2M", "3M", "4M", "5M", "6M", "7M", "8M", "9M", "10M",
                                       "11M", "1Y", "18M", "2Y", "3Y")):
    """Write fixings, policy anchors, FF futures and EFFR OIS for ``as_of``.

    ``bump``: {(instrument, contract): bp} added to the quoted rate on the as-of day.
    ``stale``: {(instrument, contract): n} repeats the as-of quote on the n-1 prior days.
    ``dead_from``: FF contracts from this index on get no open interest and no volume
    (derived settlement prices) and a price 5bp off the curve.
    Returns (true curve, quotes) with quotes {(instrument, contract): rate}."""
    m = load_manifest("usd")
    fed = m.calendar("us_fed")
    rates = load_policy_rates("fed")
    mid = rate_in_effect(rates, "target_midpoint", as_of)
    through = add_months(as_of, 37) + dt.timedelta(days=40)
    bump, stale = bump or {}, stale or {}

    # fixings: midpoint in effect + spread, month-ends bumped (rate dates before as_of)
    days = []
    d = fed.previous_business_day(as_of)
    while len(days) < history_bd:
        days.append(d)
        d = fed.previous_business_day(d)
    days = sorted(days)
    fix = {}
    for d in days:
        v = rate_in_effect(rates, "target_midpoint", d) + SYNTHETIC_SPREAD
        if fed.next_business_day(d).month != d.month:
            v += TURN_BUMP
        fix[d] = round(v, 4)
    curve = true_curve(as_of, through, mid + SYNTHETIC_SPREAD, list(steps), fix)

    quotes = {}
    ff_cols, ois_cols = {}, {}
    horizon = add_months(as_of, 36)
    live = [c for c in listed_contracts(m, "ff_fut", as_of)
            if c.first_listed <= as_of <= c.last_quote and c.ref_start < horizon]
    for i, c in enumerate(live):
        r = AverageRateFuture(m, "ff_fut", c).rate(curve) + bump.get(("ff_fut", c.contract), 0.0) / 100.0
        dead = dead_from is not None and i >= dead_from
        if dead:
            r += 0.05
        quotes[("ff_fut", c.contract)] = r
        ff_cols[f"{c.bbg_ticker}|PX_LAST"] = round(100.0 - r, 6)
        ff_cols[f"{c.bbg_ticker}|OPEN_INT"] = 0.0 if dead else oi
        ff_cols[f"{c.bbg_ticker}|PX_VOLUME"] = 0.0 if dead else oi / 5
    for t in ois_tenors:
        r = OvernightIndexSwap(m, "ois_effr", t, as_of).rate(curve) + bump.get(("ois_effr", t), 0.0) / 100.0
        quotes[("ois_effr", t)] = r
        ois_cols[f"{m.swap_ticker('ois_effr', t)}|PX_LAST"] = round(r, 8)

    # recent history for staleness: quotes move by a small amount each day except the stale ones
    hist_days = days[-8:] + [as_of]

    def frame(cols: dict, kind: str) -> pd.DataFrame:
        rows = {}
        for i, d in enumerate(hist_days):
            back = len(hist_days) - 1 - i
            row = {}
            for col, v in cols.items():
                tk = col.split("|")[0]
                key = _key(m, tk)
                n = stale.get(key, 1)
                if col.endswith("PX_LAST") and back >= n:
                    v = v + (0.001 * back if kind == "rate" else -0.001 * back)
                row[col] = v
            rows[d.isoformat()] = row
        return pd.DataFrame.from_dict(rows, orient="index")

    out = {"ff_fut": frame(ff_cols, "price"), "ois_effr": frame(ois_cols, "rate"),
           "fixings": pd.DataFrame({"FEDL01 Index|PX_LAST": {d.isoformat(): v for d, v in fix.items()}}),
           "policy_anchors": pd.DataFrame({
               "FDTR Index|PX_LAST": {d.isoformat(): rate_in_effect(rates, "target_upper", d) for d in days},
               "FDTRFTRL Index|PX_LAST": {d.isoformat(): rate_in_effect(rates, "target_lower", d) for d in days}})}
    for group, df in out.items():
        df.index.name = "date"
        for year, g in df.groupby(df.index.str[:4]):
            p = root / "usd" / year / f"{group}.csv"
            p.parent.mkdir(parents=True, exist_ok=True)
            g.sort_index().to_csv(p, lineterminator="\n")
    return curve, quotes


def _key(m, ticker: str):
    fut = m.parse_future_ticker(ticker)
    if fut:
        return (fut[0], f"{fut[1]}-{fut[2]:02d}")
    for t in m.raw["tenor_codes"]:
        if ticker == m.swap_ticker("ois_effr", t):
            return ("ois_effr", t)
    return None
