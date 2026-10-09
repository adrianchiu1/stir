"""Replica of Bloomberg WIRP's two models (the M2 gate reference; `docs/research/wirp/`).

Both models rest on one assumption: "only a central bank action will impact the
effective interest rate of an economy", so the overnight rate is flat between
effective dates (D2) and each instrument's quote is "pushed forward and backward"
through the parcels it covers. WIRP solves sequentially, one instrument at a
time, with no weights, robust loss, prior, turn or risk-premium adjustment.

Futures model ("Calculations", 9/16/2019 example): a contract month without a
meeting gives one rate; for a meeting month ``N x avg = d_pre x pre + d_post x post``
with ``pre`` carried forward from the preceding non-meeting contract and ``post``
solved; the meeting day itself is at the pre-meeting rate. OIS model (9/13/2018
example): fixed ``1 + r n/360`` against the daily-compounded float, spot lag 2
days, weekends and holidays carried; the 1W tenor gives the pre-meeting rate, the
1M the first post-meeting rate ("more liquidity than the similar three-week
security"), then the monthly tenors in turn, each assumed to carry one constant
unknown rate found by Newton's method.

The general rule implemented here reproduces those worked examples: instruments
are taken in order of window end; an instrument with one unknown parcel solves
it; one with no unknown parcel re-solves the latest parcel it covers (the
"carry the November rate forward" rule: a later, more direct quote overrides);
one with several unknowns waits until the following instruments make the system
square, which is then solved jointly. Parcels no instrument reaches stay empty:
WIRP "does not show meeting dates beyond that point".

Instrument models, calendars, day counts and conventions all come from the
manifest (``stircurve.instruments``); nothing here is USD-specific.
"""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

import numpy as np

from ..instruments import BoundInstrument
from .flat_forward import FlatForwardCurve, ParcelGrid

BUMP = 1e-4             # percent, numerical derivative
MAX_NEWTON = 60
TOL = 1e-10             # percent


@dataclass
class Equation:
    key: str
    bound: BoundInstrument
    quote: float                      # percent
    parcels: tuple[int, ...]          # parcels (indices >= 0) the instrument prices
    end: dt.date                      # window end (order of solving)


@dataclass
class ReplicaResult:
    model: str
    grid: ParcelGrid
    rates: np.ndarray                 # percent per parcel; NaN beyond the instruments' reach
    used: list[tuple[str, float]]     # (key, quote) in the order solved
    skipped: list[tuple[str, str]]    # (key, reason)
    solved_by: dict[int, str]         # parcel index -> key(s) of the equation(s) that fixed it last
    notes: list[str] = field(default_factory=list)

    @property
    def curve(self) -> FlatForwardCurve:
        return FlatForwardCurve(self.grid, np.where(np.isnan(self.rates), 0.0, self.rates))

    @property
    def current_implied(self) -> float:
        return float(self.rates[0])

    def implied(self, k: int) -> float:
        """Post-meeting implied rate of the parcel meeting ``k`` opens (NaN beyond WIRP's reach)."""
        return float(self.rates[k])


def _touched(b: BoundInstrument) -> tuple[int, ...]:
    return tuple(sorted({int(i) for rd in b.rate_days for i in rd.idx if i >= 0}))


def _priced(b: BoundInstrument, n: int, min_sensitivity: float) -> tuple[int, ...]:
    """Parcels the instrument really prices: sensitivity above ``min_sensitivity`` (an OIS paying
    two days into the next parcel touches it through discounting only; a front contract in its
    last days barely sees the stub)."""
    x = np.zeros(n)
    f0 = b.value(x)
    out = []
    for k in _touched(b):
        xb = x.copy()
        xb[k] += BUMP
        if abs((b.value(xb) - f0) / BUMP) >= min_sensitivity:
            out.append(k)
    return tuple(out)


def _solve(eqs: list[Equation], unknown: list[int], x: np.ndarray) -> tuple[np.ndarray, bool]:
    """Gauss-Newton on the square (or over-determined) system eqs(x) = quotes for x[unknown]."""
    out = x.copy()
    x = _filled(x, eqs[0].quote)       # parcels not yet solved (touched only through discounting): flat extrapolation
    ok = False
    for _ in range(MAX_NEWTON):
        f = np.array([e.bound.value(x) for e in eqs])
        r = np.array([e.quote for e in eqs]) - f
        J = np.empty((len(eqs), len(unknown)))
        for j, k in enumerate(unknown):
            xb = x.copy()
            xb[k] += BUMP
            J[:, j] = [(e.bound.value(xb) - fe) / BUMP for e, fe in zip(eqs, f)]
        step = np.linalg.lstsq(J, r, rcond=None)[0]
        x[unknown] += step
        if np.max(np.abs(step)) < TOL:
            ok = True
            break
    out[unknown] = x[unknown]
    return out, ok


def _filled(x: np.ndarray, default: float) -> np.ndarray:
    """NaN parcels take the last solved parcel before them (or the first solved one, or ``default``)."""
    y = x.copy()
    known = np.where(~np.isnan(y))[0]
    if not len(known):
        return np.full_like(y, default)
    last = y[known[0]]
    for k in range(len(y)):
        if np.isnan(y[k]):
            y[k] = last
        else:
            last = y[k]
    return y


def sequential_bootstrap(model: str, grid: ParcelGrid,
                         instruments: list[tuple[str, BoundInstrument, float, dt.date]],
                         min_sensitivity: float = 0.01) -> ReplicaResult:
    """``instruments``: (key, bound model, quoted rate in percent, window end), any order;
    they are taken in order of window end (a contract month, an OIS maturity)."""
    eqs = [Equation(k, b, q, _priced(b, grid.n, min_sensitivity), end) for k, b, q, end in instruments]
    eqs.sort(key=lambda e: (e.end, e.key))
    x = np.full(grid.n, np.nan)
    used, skipped, solved_by, notes = [], [], {}, []
    pending: list[Equation] = []
    for e in eqs:
        if not e.parcels:
            skipped.append((e.key, f"prices no parcel (sensitivity below {min_sensitivity}: window fixed, or too few days left)"))
            continue
        unknown = [k for k in e.parcels if np.isnan(x[k])]
        if pending:
            pending.append(e)
            pend_unknown = sorted({k for p in pending for k in p.parcels if np.isnan(x[k])})
            if len(pend_unknown) <= len(pending):
                x, ok = _solve(pending, pend_unknown, x)
                keys = " + ".join(p.key for p in pending)
                for k in pend_unknown:
                    solved_by[k] = keys
                used += [(p.key, p.quote) for p in pending]
                if not ok:
                    notes.append(f"{keys}: Newton did not converge")
                pending = []
            continue
        if len(unknown) == 1:
            x, ok = _solve([e], unknown, x)
            solved_by[unknown[0]] = e.key
            used.append((e.key, e.quote))
            if not ok:
                notes.append(f"{e.key}: Newton did not converge")
        elif len(unknown) == 0:
            last = max(e.parcels)          # re-solve the latest parcel this quote covers (override)
            x, ok = _solve([e], [last], x)
            solved_by[last] = e.key
            used.append((e.key, e.quote))
            notes.append(f"{e.key}: no new parcel; re-solved parcel {last} ({grid.labels[last] if grid.labels else last})")
        else:
            pending.append(e)
    for p in pending:
        skipped.append((p.key, "left unsolved: more unknown parcels than instruments after it"))
    if np.isnan(x[0]):
        known = np.where(~np.isnan(x))[0]
        if len(known):
            x[0] = x[known[0]]
            notes.append("stub parcel not identified by any instrument: set to the first solved parcel")
    return ReplicaResult(model, grid, x, used, skipped, solved_by, notes)


def wirp_outputs(res: ReplicaResult, arm: float) -> list[dict]:
    """WIRP's implied data per meeting: Post-Meeting Implied Rate, Imp. Rate Δ (vs the Current
    Implied O/N Rate), #Hikes/Cuts (Δ / A.R.M., cumulative) and %Hike/Cut (marginal step / A.R.M.)."""
    cur = res.current_implied
    out = []
    prev = cur
    for k in range(1, res.grid.n):
        imp = res.rates[k]
        if np.isnan(imp):
            out.append({"parcel": k, "implied_rate": np.nan, "imp_rate_delta": np.nan, "n_moves": np.nan,
                        "pct_move": np.nan})
            continue
        delta = imp - cur
        out.append({"parcel": k, "implied_rate": imp, "imp_rate_delta": delta, "n_moves": delta / arm,
                    "pct_move": (imp - prev) / arm * 100.0})
        prev = imp
    return out
