"""Robust IRLS (Huber) for parcel rates with Gaussian prior rows (D4).

Minimises, over parcel rates x (percent),

    sum_i  rho_k( z_i )  +  sum_j ((L_j x - c_j) / tau_j)^2 / 2,
    z_i = (quote_i - model_i(x)) * sqrt(w_i) / sigma_i            (in bp)

with rho_k the Huber loss (quadratic within k standardised units, linear beyond),
w_i the liquidity/staleness weight in (0, 1], sigma_i the quote noise of a fully
liquid, fresh quote (bp; it is the scale, fixed rather than estimated from a dozen
residuals, which is the "MAD floored at tick size" of the memo), and (L, c, tau)
the prior rows: a step prior ``x_k - x_{k-1} ~ N(0, tau_step)`` on every meeting
(weak; equal-step split where the data do not identify the steps, D4/D-C) and a
level prior on the stub. Each iteration is a Gauss-Newton step on the weighted
least-squares problem with the Huber weights min(1, k/|z_i|) held fixed
(iteratively reweighted least squares). The Jacobian is numerical (models are
cheap vectorised lookups; FF futures are linear in x).

Drop list: after convergence an observation whose Huber weight is below
``drop_weight`` is dropped and the problem refitted without it, until no new drop
appears. Identification: the share of each parcel's unit direction lying in the
row space of the weighted data Jacobian (1 = the data pin it down, 0 = only the
prior does). Leverage: the diagonal of the hat matrix of the final weighted
problem (prior rows included); a quote with leverage near 1 alone pins a parcel,
so no residual-based method can flag an error in it (Rousseeuw's masking).
``leave_one_out`` refits without each quote in turn and reprices it: the only
residual that sees a leverage-one quote.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

BUMP = 1e-4          # percent (0.01bp)
MAX_DROP_ROUNDS = 10


@dataclass
class Observation:
    key: str
    value: object        # callable x -> model rate (percent)
    target: float        # quoted rate (percent)
    sigma_bp: float
    weight: float        # liquidity x staleness, in (0, 1]


@dataclass
class Prior:
    L: np.ndarray        # (m, n)
    c: np.ndarray        # (m,) percent
    tau_bp: np.ndarray   # (m,)
    labels: list[str] = field(default_factory=list)

    @classmethod
    def steps(cls, n: int, step_tau_bp: float, stub: float, stub_tau_bp: float,
              ties: list[tuple[int, int]] = (), tie_tau_bp: float = 2.0,
              beyond_from: int | None = None, beyond_tau_bp: float = 0.5) -> "Prior":
        """Rows: x_0 ~ N(stub, stub_tau); every step x_k - x_{k-1} ~ N(0, step_tau) (weak); for each tie
        (k, k+1), step_{k+1} - step_k ~ N(0, tie_tau) (consecutive meetings nothing in the data tells apart
        move by equal steps, D-C); from ``beyond_from`` on, steps ~ N(0, beyond_tau) (flat past the last
        instrument)."""
        rows, c, tau, labels = [], [], [], []

        def row(coef: dict, target: float, t: float, label: str):
            r = np.zeros(n)
            for k, v in coef.items():
                r[k] = v
            rows.append(r)
            c.append(target)
            tau.append(float(t))
            labels.append(label)

        row({0: 1.0}, stub, stub_tau_bp, "stub level")
        for k in range(1, n):
            beyond = beyond_from is not None and k >= beyond_from
            row({k: 1.0, k - 1: -1.0}, 0.0, beyond_tau_bp if beyond else step_tau_bp,
                f"step {k}" + (" (beyond the data: flat)" if beyond else ""))
        for k, j in ties:
            if 1 <= k < j < n:
                row({j: 1.0, k: -2.0, k - 1: 1.0} if j == k + 1 else {j: 1.0, j - 1: -1.0, k: -1.0, k - 1: 1.0},
                    0.0, tie_tau_bp, f"equal steps {k} and {j}")
        return cls(np.array(rows), np.array(c), np.array(tau), labels)

@dataclass
class FitResult:
    x: np.ndarray
    model: np.ndarray            # model rate per observation (percent)
    residual_bp: np.ndarray      # quote - model
    huber_weight: np.ndarray
    dropped: list[int]           # observation indices on the drop list (in drop order)
    identification: np.ndarray   # per parcel, in [0, 1]
    leverage: np.ndarray         # per observation, in [0, 1]
    posterior_sigma_bp: np.ndarray   # per parcel, from the final information matrix
    iterations: int
    converged: bool
    rounds: list[list[int]] = field(default_factory=list)   # observations dropped in each refit round


def jacobian(obs: list[Observation], x: np.ndarray, f0: np.ndarray) -> np.ndarray:
    J = np.empty((len(obs), len(x)))
    for k in range(len(x)):
        xb = x.copy()
        xb[k] += BUMP
        J[:, k] = [(o.value(xb) - f) / BUMP for o, f in zip(obs, f0)]
    return J


def huber_weights(z: np.ndarray, k: float) -> np.ndarray:
    a = np.abs(z)
    return np.where(a <= k, 1.0, k / np.maximum(a, 1e-300))


def identification(Jw: np.ndarray, n: int, rtol: float = 1e-8) -> np.ndarray:
    """Share of each unit direction e_k in the row space of ``Jw``."""
    if Jw.size == 0:
        return np.zeros(n)
    _, s, vt = np.linalg.svd(Jw, full_matrices=False)
    r = int((s > rtol * s.max()).sum()) if s.size and s.max() > 0 else 0
    V = vt[:r]
    return np.clip((V ** 2).sum(axis=0), 0.0, 1.0)


def _solve(obs, active, x0, prior: Prior, k, max_iter, tol_bp):
    x = x0.copy()
    sig = np.array([o.sigma_bp for o in obs])
    w = np.array([o.weight for o in obs])
    tgt = np.array([o.target for o in obs])
    act = np.zeros(len(obs), bool)
    act[active] = True
    Lp = 100.0 * prior.L / prior.tau_bp[:, None]           # bp per percent
    converged, it = False, 0
    for it in range(1, max_iter + 1):
        f = np.array([o.value(x) for o in obs])
        r = (tgt - f) * 100.0
        z = r * np.sqrt(w) / sig
        hw = huber_weights(z, k)
        W = np.where(act, hw * w / sig ** 2, 0.0)
        J = jacobian(obs, x, f) * 100.0
        A = np.vstack([np.sqrt(W)[:, None] * J, Lp])
        b = np.concatenate([np.sqrt(W) * r, 100.0 * (prior.c - prior.L @ x) / prior.tau_bp])
        dx = np.linalg.lstsq(A, b, rcond=None)[0]
        x = x + dx
        if np.max(np.abs(dx)) * 100.0 < tol_bp:
            converged = True
            break
    f = np.array([o.value(x) for o in obs])
    r = (tgt - f) * 100.0
    hw = huber_weights(r * np.sqrt(w) / sig, k)
    W = np.where(act, hw * w / sig ** 2, 0.0)
    J = jacobian(obs, x, f) * 100.0
    A = np.vstack([np.sqrt(W)[:, None] * J, Lp])
    info_inv = np.linalg.pinv(A.T @ A)
    rows = (np.sqrt(w) / sig)[:, None] * J
    lev = np.einsum("ij,ij->i", rows @ info_inv, rows) * np.where(act, hw, 1.0)
    post_sigma = np.sqrt(np.clip(np.diag(info_inv), 0.0, None))      # bp
    return x, f, r, hw, np.sqrt(W)[:, None] * J, lev, post_sigma, it, converged


def fit(obs: list[Observation], prior: Prior, x0: np.ndarray, *, huber_k: float = 1.345,
        drop_weight: float = 0.2, max_iter: int = 50, tol_bp: float = 1e-5,
        active: list[int] | None = None) -> FitResult:
    x = np.asarray(x0, dtype=float).copy()
    active = list(range(len(obs))) if active is None else list(active)
    dropped: list[int] = []
    rounds: list[list[int]] = []
    total_it = 0
    for _ in range(MAX_DROP_ROUNDS):
        x, f, r, hw, Jw, lev, ps, it, conv = _solve(obs, active, x, prior, huber_k, max_iter, tol_bp)
        total_it += it
        new = [i for i in active if hw[i] < drop_weight]
        if not new:
            break
        rounds.append(new)
        dropped += new
        active = [i for i in active if i not in new]
    lev = np.clip(lev, 0.0, 1.0)
    inactive = [i for i in range(len(obs)) if i not in active]
    lev[inactive] = np.nan            # not part of the final problem
    return FitResult(x, f, r, hw, dropped, identification(Jw, len(x)), lev, ps, total_it, conv, rounds)


def loss(obs: list[Observation], active: list[int], x: np.ndarray, huber_k: float) -> float:
    """Robust loss sum rho_k(z_i) over ``active`` at ``x`` (in standardised units)."""
    tot = 0.0
    for i in active:
        o = obs[i]
        z = abs((o.target - o.value(x)) * 100.0) * np.sqrt(o.weight) / o.sigma_bp
        tot += 0.5 * z * z if z <= huber_k else huber_k * (z - 0.5 * huber_k)
    return float(tot)


def refit_without(obs: list[Observation], prior: Prior, x0: np.ndarray, active: list[int], drop: int,
                  **kw) -> tuple[np.ndarray, np.ndarray]:
    """(parcel rates, identification per parcel) refitted with ``drop`` left out (no drop rounds)."""
    others = [j for j in active if j != drop]
    r = _solve(obs, others, x0, prior, kw.get("huber_k", 1.345), kw.get("max_iter", 50), kw.get("tol_bp", 1e-5))
    return r[0], identification(r[4], len(x0))


def leave_one_out(obs: list[Observation], prior: Prior, res: FitResult, active: list[int] | None = None,
                  **kw) -> np.ndarray:
    """Prediction residual (bp) of each active quote when the curve is fitted without it; NaN for the rest."""
    active = [i for i in range(len(obs)) if i not in res.dropped] if active is None else list(active)
    out = np.full(len(obs), np.nan)
    for i in active:
        others = [j for j in active if j != i]
        r = _solve(obs, others, res.x, prior, kw.get("huber_k", 1.345), kw.get("max_iter", 50), kw.get("tol_bp", 1e-5))
        out[i] = (obs[i].target - obs[i].value(r[0])) * 100.0
    return out
