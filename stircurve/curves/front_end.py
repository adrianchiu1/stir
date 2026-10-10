"""EFFR-family front end for one as-of date (M2; D2, D4, D7, D11; AC's answers in PR #4).

1. Inputs (``market_inputs``): the as-of day's quotes of the family's instruments
   from the loader's tidy frame, with open interest, volume, a staleness run and
   the loader's listing findings; the fixings and the policy anchors
   (``data/refdata/policy_rates``). Instruments beyond the front-end horizon or
   with no quote are skipped, with a reason.
2. One step curve per instrument (``front_end.curves`` in usd.yaml: ``effr_fut``
   on FF futures, ``effr_ois`` on EFFR OIS). FF futures and OIS are separate
   instruments with a basis between them (AC); the basis is a diagnostic (D5).
3. Nodes (``curves.nodes``): one parcel per meeting effective date after the
   as-of date: published meetings, synthetic ones to the horizon (flagged),
   decided unscheduled meetings from their decision date, superseded meetings
   until their supersession date. Month-ends are never nodes.
4. Replica (``curves.wirp_replica``): WIRP's sequential bootstrap on the same
   quotes, the gate reference (layer 1 of the validation).
5. Fit (``curves.robust``): per curve, robust IRLS with Huber loss, liquidity
   and staleness weights, metadata exclusions (an FF price with no open interest
   and no volume is a derived settlement price, not a quote), a weak step prior
   (equal-step split beyond the data's reach, D-C) and a weak stub prior
   (anchor + spread, D7); drop list, identification, leverage, leave-one-out.
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from ..config.loader import load_config
from ..marketdata import loader
from ..marketdata.contracts import listed_contracts
from ..marketdata.dump import MARKET_DIR
from ..marketdata.manifest import Manifest, load_manifest
from ..policy.spread import SpreadEstimate, policy_spread, turn_days
from ..refdata.calendars import add_months, parse_tenor
from ..refdata.maintenance import PolicyRate, load_policy_rates, rate_in_effect
from ..refdata.meetings import Meeting, MeetingSchedule
from ..instruments import AverageRateFuture, OvernightIndexSwap
from . import robust
from .flat_forward import FlatForwardCurve, ParcelGrid
from .nodes import build_grid, meeting_nodes
from .wirp_replica import ReplicaResult, _priced, sequential_bootstrap

HISTORY_DAYS = 130            # calendar days of history loaded before the as-of date (63bd spread window, staleness)
CURVE_TAIL_DAYS = 7           # the last parcel runs this far past the last instrument date
MAX_LOO_DROPS = 3             # quotes dropped on their leave-one-out residual, one at a time, largest first


# ---------------------------------------------------------------------------
# inputs
# ---------------------------------------------------------------------------
@dataclass
class InstrumentQuote:
    instrument: str
    contract: str            # 'YYYY-MM' or tenor
    ticker: str
    px: float                # quote as on file (price or rate)
    rate: float              # quoted rate, percent
    model: object            # AverageRateFuture | OvernightIndexSwap
    start: dt.date
    end: dt.date
    open_interest: float = np.nan
    volume: float = np.nan
    stale_run: int = 1       # consecutive observations with this value, ending on the as-of date
    stale: bool = False
    notes: list[str] = field(default_factory=list)

    @property
    def key(self) -> str:
        return f"{self.instrument} {self.contract}"

    @property
    def has_activity(self) -> bool:
        """Open interest or volume above zero (NaN: the field was not dumped for this contract)."""
        return bool((np.isfinite(self.open_interest) and self.open_interest > 0)
                    or (np.isfinite(self.volume) and self.volume > 0))


@dataclass
class Skipped:
    instrument: str
    contract: str
    ticker: str
    reason: str


@dataclass
class MarketInputs:
    as_of: dt.date
    quotes: list[InstrumentQuote]
    skipped: list[Skipped]
    fixings: pd.Series                  # index: rate dates (Timestamp), percent
    policy_rates: list[PolicyRate]
    loader_report: loader.Report


def _run_length(s: pd.Series) -> int:
    v = s.dropna().to_numpy()
    if not len(v):
        return 0
    n = 1
    while n < len(v) and v[-1 - n] == v[-1]:
        n += 1
    return n


def curve_instruments(cfg: dict) -> list[str]:
    out: list[str] = []
    for spec in cfg["front_end"]["curves"].values():
        out += [i for i in spec["instruments"] if i not in out]
    return out


def market_inputs(m: Manifest, cfg: dict, as_of: dt.date, root: Path = MARKET_DIR,
                  frame: pd.DataFrame | None = None, report: loader.Report | None = None) -> MarketInputs:
    fe = cfg["front_end"]
    if frame is None:
        frame, report = loader.load(m, as_of - dt.timedelta(days=HISTORY_DAYS), as_of, root)
    report = report or loader.Report()
    ts = pd.Timestamp(as_of)
    hist = frame[frame["date"] <= ts]
    today = hist[hist["date"] == ts]
    horizon = add_months(as_of, 12 * fe["horizon_years"])
    quotes: list[InstrumentQuote] = []
    skipped: list[Skipped] = []
    findings = {k: [x for x in report.found.get(k, [])] for k in ("outside_listing", "outside_listing_unverified")}
    mea = fe.get("month_end_adjustment", {})
    fix_cal = m.calendar(m.fixings[fe["spread"]["fixing"]]["calendar"])
    turns = tuple(sorted(turn_days(fix_cal, as_of, add_months(horizon, 3)))) if mea.get("enabled") else ()
    adj_bp = float(mea.get("dip_bp", 0.0)) if mea.get("enabled") else 0.0

    for name in curve_instruments(cfg):
        ins = m.instruments[name]
        sub = today[today["instrument"] == name]
        px = sub[sub["field"] == ins["fields"][0]].set_index("contract")["value"]
        oi = sub[sub["field"] == "OPEN_INT"].set_index("contract")["value"]
        vol = sub[sub["field"] == "PX_VOLUME"].set_index("contract")["value"]
        h = hist[(hist["instrument"] == name) & (hist["field"] == ins["fields"][0])]
        if ins["kind"] == "future":
            every = {c.contract: c for c in listed_contracts(m, name, as_of, "dump_listing")}
            listed = {c.contract for c in listed_contracts(m, name, as_of) if c.first_listed <= as_of <= c.last_quote}
            wanted = sorted((set(px.index) | listed) & set(every))
            for con in wanted:
                c = every[con]
                tk = c.bbg_ticker
                if c.ref_end <= as_of:
                    skipped.append(Skipped(name, con, tk, "reference window fully fixed"))
                    continue
                if c.ref_start >= horizon:
                    if con in px.index:
                        skipped.append(Skipped(name, con, tk, f"beyond the front-end horizon ({horizon})"))
                    continue
                if con not in px.index:
                    skipped.append(Skipped(name, con, tk, "no quote on the as-of date"))
                    continue
                model = AverageRateFuture(m, name, c, adj_bp, turns)
                q = InstrumentQuote(name, con, tk, float(px[con]), model.rate_from_quote(float(px[con])), model,
                                    c.ref_start, c.ref_end, float(oi.get(con, np.nan)), float(vol.get(con, np.nan)))
                if con not in listed:
                    q.notes.append("quoted outside the modelled exchange listing (unverified schedule): used")
                quotes.append(q)
        else:
            max_months = 12 * fe["horizon_years"]
            for tenor in ins["tenors"]:
                months, _, weeks = parse_tenor(tenor)
                tk = m.swap_ticker(name, tenor)
                if months > max_months:
                    if tenor in px.index:
                        skipped.append(Skipped(name, tenor, tk, f"beyond the front end ({fe['horizon_years']}y; back end is M4)"))
                    continue
                if tenor not in px.index:
                    skipped.append(Skipped(name, tenor, tk, "no quote on the as-of date"))
                    continue
                model = OvernightIndexSwap(m, name, tenor, as_of)
                quotes.append(InstrumentQuote(name, tenor, tk, float(px[tenor]), model.rate_from_quote(float(px[tenor])),
                                              model, model.start, model.end))
        n_stale = ins.get("stale_days")
        for q in quotes:
            if q.instrument != name:
                continue
            q.stale_run = _run_length(h[h["contract"] == q.contract].set_index("date")["value"])
            q.stale = bool(n_stale and q.stale_run >= n_stale)
            if q.stale:
                q.notes.append(f"stale: unchanged {q.stale_run} observations (>= {n_stale})")
            for msg in findings["outside_listing_unverified"]:
                if f"{q.ticker}|" in msg:
                    q.notes.append("loader: " + msg.split(": ", 1)[-1])

    # quotes the loader removed (blocking: quoted outside a verified listing) on the as-of date
    for msg in findings["outside_listing"]:
        if as_of.isoformat() in msg:
            tk = msg.split(as_of.isoformat(), 1)[1].strip().split("|", 1)[0]     # '<ticker>|<field> after ...'
            hit = m.parse_future_ticker(tk)
            if hit and hit[0] in curve_instruments(cfg):
                skipped.append(Skipped(hit[0], f"{hit[1]}-{hit[2]:02d}", tk, "loader: " + msg.split(": ", 1)[-1]))

    fix = hist[(hist["instrument"] == fe["spread"]["fixing"]) & (hist["field"] == "PX_LAST")]
    fixings = fix.set_index("date")["value"].sort_index()
    return MarketInputs(as_of, quotes, skipped, fixings, load_policy_rates(cfg["bank"]), report)


# ---------------------------------------------------------------------------
# one curve
# ---------------------------------------------------------------------------
@dataclass
class CurveFit:
    name: str
    instruments: list[str]
    as_of: dt.date
    meetings: list[Meeting]
    grid: ParcelGrid
    curve: FlatForwardCurve
    curve_end: dt.date
    prior: robust.Prior
    stub_prior: float
    stub_prior_source: str
    fit: robust.FitResult
    used: list[InstrumentQuote]             # quotes that entered the fit (dropped ones included, see fit.dropped)
    excluded: list[tuple[InstrumentQuote, str]]
    weights: np.ndarray                     # liquidity x staleness per used quote
    liquidity: np.ndarray
    sigma_bp: np.ndarray
    loo_bp: np.ndarray                      # leave-one-out prediction residual per used quote
    replica: ReplicaResult
    replica_quotes: list[InstrumentQuote]   # quotes the replica was offered
    missing_fixings: list[dt.date]
    loo_dropped: list[int] = field(default_factory=list)   # indices into ``used`` dropped on leave-one-out residuals

    @property
    def dropped(self) -> list[int]:
        """Every quote the fit left out (robust weight, then leave-one-out), indices into ``used``."""
        return list(self.fit.dropped) + list(self.loo_dropped)

    @property
    def wirp_reach(self) -> int:
        """Number of meetings the replica prices (WIRP's reach on this instrument)."""
        return int(np.sum(~np.isnan(self.replica.rates[1:])))


def liquidity_weight(q: InstrumentQuote, spec: dict | None) -> tuple[float, str | None]:
    """(weight, exclusion reason)."""
    if not spec:
        return 1.0, None
    if not q.has_activity:
        if spec.get("exclude_without_any"):
            return 0.0, "no open interest and no volume: a derived settlement price, not a quote"
        q.notes.append("no open interest or volume: liquidity floor")
        return float(spec["floor"]), None
    ratios = [r for r in (q.open_interest / spec["open_interest_full"], q.volume / spec["volume_full"])
              if np.isfinite(r)]
    return float(np.clip(max(ratios), spec["floor"], 1.0)), None


def _replica_quotes(cfg: dict, name: str, quotes: list[InstrumentQuote]) -> list[InstrumentQuote]:
    spec = cfg["front_end"]["curves"][name]
    w = cfg["front_end"]["wirp"]
    model = spec["wirp_model"]
    if model == "futures":
        f = w["futures"]
        return [q for q in quotes if q.instrument == f["instrument"] and (q.has_activity or not f["require_activity"])]
    if model == "ois":
        o = w["ois"]
        out = []
        for q in quotes:
            if q.instrument != o["instrument"] or q.contract in o.get("skip_tenors", []):
                continue
            months, _, weeks = parse_tenor(q.contract)
            if months <= o["max_tenor_months"]:
                out.append(q)
        return out
    raise ValueError(f"{name}: wirp_model {model!r}")


def build_curve(name: str, cfg: dict, m: Manifest, inputs: MarketInputs, spread: SpreadEstimate,
                anchor_now: float | None, schedule: MeetingSchedule | None = None) -> CurveFit:
    fe, fit_cfg = cfg["front_end"], cfg["front_end"]["fit"]
    spec = fe["curves"][name]
    as_of = inputs.as_of
    quotes = [q for q in inputs.quotes if q.instrument in spec["instruments"]]
    if not quotes:
        raise ValueError(f"{as_of}: no {spec['instruments']} quotes on file for curve {name}")

    # metadata exclusions and weights
    used, excluded, liq = [], [], []
    for q in quotes:
        lo, hi = m.instruments[q.instrument]["valid_range"]
        if not (lo <= q.px <= hi):
            excluded.append((q, f"quote {q.px} outside the manifest's valid range [{lo}, {hi}]: not a price"))
            continue
        w, why = liquidity_weight(q, fit_cfg.get("liquidity", {}).get(q.instrument))
        if why:
            excluded.append((q, why))
        else:
            used.append(q)
            liq.append(w)
    # the strip's reach ends at its first contract without open interest or volume: an isolated active
    # contract beyond a dead stretch is a quote nothing can check (WIRP: "if there is no reliable pricing on
    # all monthly tenors beyond a certain point on the curve, WIRP does not show meeting dates beyond that point")
    dead_from = {}
    for q, why in excluded:
        if "derived settlement price" in why:
            dead_from[q.instrument] = min(dead_from.get(q.instrument, q.start), q.start)
    keep, keep_liq = [], []
    for q, w in zip(used, liq):
        if q.instrument in dead_from and q.start > dead_from[q.instrument]:
            excluded.append((q, f"beyond the strip's reach (first contract without open interest or volume starts "
                                f"{dead_from[q.instrument]})"))
        else:
            keep.append(q)
            keep_liq.append(w)
    used, liq = keep, keep_liq
    if not used:
        raise ValueError(f"{as_of}: every {spec['instruments']} quote excluded for curve {name}")
    liq = np.array(liq)

    # grid
    horizon = add_months(as_of, 12 * fe["horizon_years"])
    last_needed = max([q.end for q in used] + [p for q in used for p in getattr(q.model, "payments", [])])
    curve_end = max(horizon, last_needed + dt.timedelta(days=CURVE_TAIL_DAYS))
    meetings = meeting_nodes(cfg, as_of, curve_end, schedule)
    grid = build_grid(as_of, meetings, inputs.fixings)
    bound = [q.model.bind(grid) for q in used]
    missing = sorted({d for b in bound for d in b.missing_fixings})

    # replica (WIRP's sequential bootstrap) on the quotes WIRP would use
    rq = _replica_quotes(cfg, name, used)
    replica = sequential_bootstrap(spec["wirp_model"], grid,
                                   [(q.key, q.model.bind(grid), q.rate, q.end) for q in rq],
                                   min_sensitivity=fe["wirp"].get("min_sensitivity", 0.025))

    # prior: weak steps, weak stub level (anchor + spread, else the last fixing)
    if anchor_now is not None and spread.value is not None:
        stub, src = anchor_now + spread.value, "anchor + spread (D7)"
    elif len(inputs.fixings.dropna()):
        stub, src = float(inputs.fixings.dropna().iloc[-1]), "last fixing"
    else:
        stub, src = float(used[0].rate), "front quote"
    ties, beyond = prior_structure(grid, [q.end for q in used])
    prior = robust.Prior.steps(grid.n, fit_cfg["step_prior_sigma_bp"], stub, fit_cfg["stub_prior_sigma_bp"],
                               ties, fit_cfg["tie_sigma_bp"], beyond, fit_cfg["beyond_data_sigma_bp"])
    x0 = replica.rates.copy()
    if np.isnan(x0[0]):
        x0[0] = stub
    for k in range(1, grid.n):            # flat extrapolation beyond the replica's reach
        if np.isnan(x0[k]):
            x0[k] = x0[k - 1]

    stale = np.array([fit_cfg["stale_multiplier"] if q.stale else 1.0 for q in used])
    sig = np.array([fit_cfg["quote_sigma_bp"][q.instrument] for q in used], dtype=float)
    obs = [robust.Observation(q.key, b.value, q.rate, s, w) for q, b, s, w in zip(used, bound, sig, liq * stale)]
    kw = dict(huber_k=fit_cfg["huber_k"], max_iter=fit_cfg["max_iter"], tol_bp=fit_cfg["tol_bp"])
    priced = [set(_priced(b, grid.n, fe["wirp"].get("min_sensitivity", 0.025))) for b in bound]
    active = list(range(len(obs)))
    loo_dropped: list[int] = []
    loo_at_drop: dict[int, float] = {}
    scale = sig / np.sqrt(liq * stale)                 # effective quote noise in bp (weight folded in)
    for _ in range(MAX_LOO_DROPS + 1):
        res = robust.fit(obs, prior, x0, drop_weight=fit_cfg["drop_weight"], active=active, **kw)
        active = [i for i in active if i not in res.dropped]
        loo = robust.leave_one_out(obs, prior, res, active, **kw)
        # a quote that alone pins a parcel hides its error from every residual but the leave-one-out one; its
        # good neighbours show large leave-one-out residuals too (masking), so among the candidates (standardised
        # by the quote's effective noise) the one whose removal leaves the smallest robust loss on the rest is
        # the culprit
        cands = [i for i in active if np.isfinite(loo[i]) and abs(loo[i]) / scale[i] > fit_cfg["loo_drop_z"]
                 and _others_cover(i, active, priced)]
        if not cands or len(loo_dropped) >= MAX_LOO_DROPS:
            break
        rest_loss = {}
        for i in cands:
            x_wo, pred_sigma = robust.refit_without(obs, prior, res.x, active, i, **kw)
            # the residual is evidence against the quote only relative to what the rest knows about it: a lone
            # 2Y OIS, or a contract whose parcel the others see for two days, is not an outlier
            if abs(loo[i]) / np.sqrt(scale[i] ** 2 + pred_sigma ** 2) > fit_cfg["loo_drop_z"]:
                rest_loss[i] = robust.loss(obs, [j for j in active if j != i], x_wo, fit_cfg["huber_k"])
        if not rest_loss:
            break
        worst = min(rest_loss, key=rest_loss.get)
        loo_dropped.append(worst)
        loo_at_drop[worst] = float(loo[worst])
        active = [i for i in active if i != worst]
        x0 = res.x
    for i, v in loo_at_drop.items():
        loo[i] = v
    return CurveFit(name, list(spec["instruments"]), as_of, meetings, grid, FlatForwardCurve(grid, res.x), curve_end,
                    prior, stub, src, res, used, excluded, liq * stale, liq, sig, loo, replica, rq, missing, loo_dropped)


def _others_cover(i: int, active: list[int], priced: list[set]) -> bool:
    """Is every parcel quote ``i`` prices also priced by another active quote? If not, its leave-one-out
    residual measures the prior's extrapolation, not the quote's error (a lone 2Y OIS is not an outlier)."""
    others = set().union(*(priced[j] for j in active if j != i)) if len(active) > 1 else set()
    return bool(priced[i]) and priced[i] <= others


def prior_structure(grid: ParcelGrid, ends: list[dt.date]) -> tuple[list[tuple[int, int]], int | None]:
    """Equal-step ties and the first parcel beyond the data. Consecutive steps k, k+1 are tied when no
    instrument ends inside parcel k (nothing in the data tells the two meetings apart); steps of parcels
    starting on or after the last instrument end are flat."""
    ends = sorted(ends)
    last = ends[-1] if ends else grid.as_of
    ties = []
    for k in range(1, grid.n - 1):
        a, b = grid.starts[k], grid.starts[k + 1]
        if not any(a <= e < b for e in ends):
            ties.append((k, k + 1))
    beyond = next((k for k in range(1, grid.n) if grid.starts[k] >= last), None)
    return ties, beyond


# ---------------------------------------------------------------------------
# the front end: every curve of the family
# ---------------------------------------------------------------------------
@dataclass
class FrontEnd:
    as_of: dt.date
    ccy: str
    cfg: dict
    inputs: MarketInputs
    spread: SpreadEstimate
    anchor_now: float | None
    curves: dict[str, CurveFit]

    @property
    def family(self) -> str:
        return self.cfg["front_end"]["family"]


def build(as_of: dt.date, ccy: str = "usd", m: Manifest | None = None, cfg: dict | None = None,
          inputs: MarketInputs | None = None, schedule: MeetingSchedule | None = None,
          root: Path = MARKET_DIR, curves: list[str] | None = None) -> FrontEnd:
    m = m or load_manifest(ccy)
    cfg = cfg or load_config(ccy)
    fe = cfg["front_end"]
    inputs = inputs or market_inputs(m, cfg, as_of, root)
    fix_cal = m.calendar(m.fixings[fe["spread"]["fixing"]]["calendar"])
    sp = fe["spread"]
    spread = policy_spread(inputs.fixings, inputs.policy_rates, sp["anchor"], fix_cal, as_of, sp["window_bd"],
                           tuple(sp["turn_days"]), sp["estimator"], tuple(sp["winsor"]), sp["min_obs"])
    anchor_now = rate_in_effect(inputs.policy_rates, sp["anchor"], as_of)
    out: dict[str, CurveFit] = {}
    for name in curves or list(fe["curves"]):
        out[name] = build_curve(name, cfg, m, inputs, spread, anchor_now, schedule)
    return FrontEnd(as_of, ccy, cfg, inputs, spread, anchor_now, out)
