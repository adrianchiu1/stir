"""EFFR-family front end for one as-of date (M2; D2, D4, D7, D11).

1. Inputs (``market_inputs``): the as-of day's quotes of the family's
   instruments from the loader's tidy frame, with open interest, volume, a
   staleness run and the loader's listing findings; the fixings and the policy
   anchors (``data/refdata/policy_rates``). Instruments beyond the front-end
   horizon (``front_end.horizon_years``) or with no quote are skipped, with a
   reason.
2. Nodes (``front_end_meetings``, ``build_grid``): one parcel per meeting
   effective date after the as-of date, from the committed meetings (published
   implementation dates already win there, D15-D18), synthetic meetings from
   cadence extrapolation to the horizon (flagged, D2), unscheduled decisions
   from their announcement date (no look-ahead, D11).
3. Prior (``ois_split``): the OIS family's split (D4), a flat-forward bootstrap
   of the OIS quotes alone, averaged over each parcel; the stub parcel (as-of
   to the first effective date) takes the anchor in effect plus the policy
   spread (D7).
4. Fit (``build``): robust IRLS with Huber loss and liquidity/staleness weights
   (``stircurve.curves.robust``), drop list, identification per parcel.
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
from ..policy.spread import SpreadEstimate, policy_spread
from ..refdata.calendars import add_months, parse_tenor
from ..refdata.maintenance import PolicyRate, load_policy_rates, rate_in_effect
from ..refdata.meetings import Meeting, MeetingSchedule
from ..instruments import AverageRateFuture, OvernightIndexSwap
from . import robust
from .flat_forward import FlatForwardCurve, ParcelGrid

HISTORY_DAYS = 130            # calendar days of history loaded before the as-of date (63bd spread window, staleness)
CURVE_TAIL_DAYS = 7           # the last parcel runs this far past the last instrument date


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


def _ticker(m: Manifest, name: str, contract: str) -> str:
    ins = m.instruments[name]
    if ins["kind"] == "future":
        y, mo = map(int, contract.split("-"))
        return m.future_ticker(name, y, mo)
    return m.swap_ticker(name, contract)


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

    for name in fe["fit"]["instruments"]:
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
                model = AverageRateFuture(m, name, c)
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
            col = msg.split(as_of.isoformat(), 1)[1].strip().split(" ", 1)
            tk = col[0].split("|")[0] if col else ""
            hit = m.parse_future_ticker(tk) if tk else None
            if hit and hit[0] in fe["fit"]["instruments"]:
                skipped.append(Skipped(hit[0], f"{hit[1]}-{hit[2]:02d}", tk, "loader: " + msg.split(": ", 1)[-1]))

    fix = hist[(hist["instrument"] == fe["spread"]["fixing"]) & (hist["field"] == "PX_LAST")]
    fixings = fix.set_index("date")["value"].sort_index()
    return MarketInputs(as_of, quotes, skipped, fixings, load_policy_rates(cfg["bank"]), report)


# ---------------------------------------------------------------------------
# nodes
# ---------------------------------------------------------------------------
def front_end_meetings(cfg: dict, as_of: dt.date, through: dt.date,
                       schedule: MeetingSchedule | None = None) -> list[Meeting]:
    """Meetings whose effective date falls in (as_of, through)."""
    sched = schedule or MeetingSchedule(cfg["bank"])
    ms = sched.with_synthetic(through, cfg["meetings"]["expected_per_year"])
    rule = cfg["front_end"]["unscheduled"]
    if rule not in ("from_decision_date", "always"):
        raise ValueError(f"front_end.unscheduled {rule!r}")
    keep = [x for x in ms if x.scheduled or rule == "always" or x.decision_date <= as_of]
    out, seen = [], set()
    for x in sorted(keep, key=lambda x: (x.effective_date, x.decision_date)):
        if as_of < x.effective_date < through and x.effective_date not in seen:
            seen.add(x.effective_date)
            out.append(x)
    return out


def build_grid(as_of: dt.date, meetings: list[Meeting], fixings: pd.Series) -> ParcelGrid:
    fx = {pd.Timestamp(d).date(): float(v) for d, v in fixings.dropna().items() if pd.Timestamp(d).date() < as_of}
    starts = (as_of,) + tuple(x.effective_date for x in meetings)
    labels = ("stub",) + tuple(x.decision_date.isoformat() + (" (synthetic)" if x.synthetic else "")
                               + ("" if x.scheduled else " (unscheduled)") for x in meetings)
    return ParcelGrid(as_of, starts, fx, labels)


# ---------------------------------------------------------------------------
# prior: the OIS family's split (D4)
# ---------------------------------------------------------------------------
def ois_split(as_of: dt.date, swaps: list[tuple[OvernightIndexSwap, float]], fixings: dict[dt.date, float],
              tol: float = 1e-10) -> FlatForwardCurve | None:
    """Flat forwards between OIS end dates, bootstrapped from the OIS quotes alone."""
    swaps = sorted(swaps, key=lambda s: s[0].end)
    ends, use = [], []
    for s, q in swaps:
        if ends and s.end <= ends[-1]:
            continue
        ends.append(s.end)
        use.append((s, q))
    if not use:
        return None
    grid = ParcelGrid(as_of, (as_of,) + tuple(ends[:-1]), fixings)
    bound = [s.bind(grid) for s, _ in use]
    x = np.full(grid.n, use[0][1])
    for i, (b, (_, q)) in enumerate(zip(bound, use)):
        r = x[i - 1] if i else q
        for _ in range(50):
            x[i:] = r
            f = b.value(x)
            x[i:] = r + 1e-4
            d = (b.value(x) - f) / 1e-4
            step = (q - f) / d
            r += step
            if abs(step) < tol:
                break
        x[i:] = r
    return FlatForwardCurve(grid, x)


def parcel_averages(curve: FlatForwardCurve, grid: ParcelGrid, last: dt.date, calendar) -> np.ndarray:
    """Calendar-day average of ``curve`` over each parcel of ``grid`` (the last closed at ``last``)."""
    out = []
    for a, b in zip(grid.starts, grid.ends(last)):
        rd = curve.grid.rate_days(a, max(b, a + dt.timedelta(days=1)), calendar, "ACT/360", "calendar_day")
        out.append(rd.average(curve.rates))
    return np.array(out)


# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------
@dataclass
class FrontEnd:
    as_of: dt.date
    ccy: str
    cfg: dict
    inputs: MarketInputs
    meetings: list[Meeting]
    grid: ParcelGrid
    curve: FlatForwardCurve
    curve_end: dt.date
    prior: np.ndarray
    prior_source: list[str]
    split: FlatForwardCurve | None
    spread: SpreadEstimate
    anchor_now: float | None
    used: list[InstrumentQuote]
    weights: np.ndarray            # liquidity x staleness per used quote
    liquidity: np.ndarray
    sigma_bp: np.ndarray
    fit: robust.FitResult
    missing_fixings: list[dt.date]


def liquidity_weight(q: InstrumentQuote, spec: dict | None) -> float:
    if not spec:
        return 1.0
    ratios = [r for r in (q.open_interest / spec["open_interest_full"], q.volume / spec["volume_full"])
              if np.isfinite(r)]
    if not ratios:
        q.notes.append("no open interest or volume: liquidity floor")
        return float(spec["floor"])
    return float(np.clip(max(ratios), spec["floor"], 1.0))


def build(as_of: dt.date, ccy: str = "usd", m: Manifest | None = None, cfg: dict | None = None,
          inputs: MarketInputs | None = None, schedule: MeetingSchedule | None = None,
          root: Path = MARKET_DIR) -> FrontEnd:
    m = m or load_manifest(ccy)
    cfg = cfg or load_config(ccy)
    fe, fit_cfg = cfg["front_end"], cfg["front_end"]["fit"]
    inputs = inputs or market_inputs(m, cfg, as_of, root)
    used = list(inputs.quotes)
    if not used:
        raise ValueError(f"{as_of}: no {fe['family']} quotes on file")

    fix_cal = m.calendar(m.fixings[fe["spread"]["fixing"]]["calendar"])
    horizon = add_months(as_of, 12 * fe["horizon_years"])
    last_needed = max([q.end for q in used] + [p for q in used for p in getattr(q.model, "payments", [])])
    curve_end = max(horizon, last_needed + dt.timedelta(days=CURVE_TAIL_DAYS))
    meetings = front_end_meetings(cfg, as_of, curve_end, schedule)
    grid = build_grid(as_of, meetings, inputs.fixings)

    # spread (D7) and the anchor in effect
    sp = fe["spread"]
    spread = policy_spread(inputs.fixings, inputs.policy_rates, sp["anchor"], fix_cal, as_of, sp["window_bd"],
                           tuple(sp["turn_days"]), sp["estimator"], tuple(sp["winsor"]), sp["min_obs"])
    anchor_now = rate_in_effect(inputs.policy_rates, sp["anchor"], as_of)

    # prior: OIS split; stub = anchor + spread
    swaps = [(q.model, q.rate) for q in used if isinstance(q.model, OvernightIndexSwap)]
    split = ois_split(as_of, swaps, grid.fixings)
    if split is not None:
        prior = parcel_averages(split, grid, curve_end, fix_cal)
        source = ["ois_split"] * grid.n
    else:
        base = anchor_now + (spread.value or 0.0) if anchor_now is not None else used[0].rate
        prior = np.full(grid.n, base)
        source = ["flat: no OIS quotes"] * grid.n
    if anchor_now is not None and spread.value is not None:
        prior[0] = anchor_now + spread.value
        source[0] = "anchor + spread"

    # observations
    liq = np.array([liquidity_weight(q, fit_cfg.get("liquidity", {}).get(q.instrument)) for q in used])
    stale = np.array([fit_cfg["stale_multiplier"] if q.stale else 1.0 for q in used])
    sig = np.array([fit_cfg["quote_sigma_bp"][q.instrument] for q in used], dtype=float)
    bound = [q.model.bind(grid) for q in used]
    obs = [robust.Observation(f"{q.instrument} {q.contract}", b.value, q.rate, s, w)
           for q, b, s, w in zip(used, bound, sig, liq * stale)]
    res = robust.fit(obs, prior, fit_cfg["prior_sigma_bp"], huber_k=fit_cfg["huber_k"],
                     drop_weight=fit_cfg["drop_weight"], max_iter=fit_cfg["max_iter"], tol_bp=fit_cfg["tol_bp"])
    missing = sorted({d for b in bound for d in b.missing_fixings})
    return FrontEnd(as_of, ccy, cfg, inputs, meetings, grid, FlatForwardCurve(grid, res.x), curve_end, prior, source,
                    split, spread, anchor_now, used, liq * stale, liq, sig, res, missing)
