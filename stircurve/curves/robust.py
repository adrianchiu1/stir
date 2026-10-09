"""Robust IRLS (Huber) for parcel rates with a Gaussian prior (D4).

Minimises, over parcel rates x (percent),

    sum_i  rho_k( z_i )  +  sum_k ((x_k - prior_k) / prior_sigma_k)^2 / 2,
    z_i = (quote_i - model_i(x)) * sqrt(w_i) / sigma_i            (in bp)

with rho_k the Huber loss (quadratic within k standardised units, linear beyond),
w_i the liquidity/staleness weight in (0, 1] and sigma_i the quote noise of a
fully liquid, fresh quote. Each iteration is a Gauss-Newton step on the
weighted least-squares problem with Huber weights min(1, k/|z_i|) held fixed
(iteratively reweighted least squares). The Jacobian is numerical (models are
cheap vectorised lookups; FF futures are linear in x).

Drop list: after convergence an observation whose Huber weight is below
``drop_weight`` is dropped and the problem refitted without it, until no new
drop appears. Identification: the share of each parcel's unit direction lying
in the row space of the weighted data Jacobian (1 = the data pin it down, 0 =
only the prior does); parcels below ``identified_threshold`` are
under-identified and their value comes from the prior's split (D4).

The prior is a smooth (Tikhonov) pull: it also biases parcels the data identify,
by about (sigma_quote / prior_sigma)^2 of the prior gap per quote pinning them
(0.04bp for a 33bp gap at 0.5bp / 10bp; the OIS-split prior is usually within a
few bp, so ~0.01bp). The identification table reports fitted minus prior.

Leverage: the diagonal of the hat matrix of the final weighted problem (prior
rows included). A quote with leverage near 1 alone pins a parcel: an error in it
moves the parcel instead of leaving a residual, so no residual-based method
(Huber included) can flag it, and its neighbours take the blame. The drop-list
review reads residuals together with leverage.
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
class FitResult:
    x: np.ndarray
    model: np.ndarray            # model rate per observation (percent)
    residual_bp: np.ndarray      # quote - model
    huber_weight: np.ndarray
    dropped: list[int]           # observation indices on the drop list (in drop order)
    identification: np.ndarray   # per parcel, in [0, 1]
    leverage: np.ndarray         # per observation, in [0, 1]
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


def identification(Jw: np.ndarray, rtol: float = 1e-8) -> np.ndarray:
    """Share of each unit direction e_k in the row space of ``Jw``."""
    n = Jw.shape[1]
    if Jw.size == 0:
        return np.zeros(n)
    _, s, vt = np.linalg.svd(Jw, full_matrices=False)
    r = int((s > rtol * s.max()).sum()) if s.size and s.max() > 0 else 0
    V = vt[:r]
    return np.clip((V ** 2).sum(axis=0), 0.0, 1.0)


def _solve(obs, active, x0, prior, prior_sigma_bp, k, max_iter, tol_bp):
    x = x0.copy()
    sig = np.array([o.sigma_bp for o in obs])
    w = np.array([o.weight for o in obs])
    tgt = np.array([o.target for o in obs])
    act = np.zeros(len(obs), bool)
    act[active] = True
    hw = np.ones(len(obs))
    converged, it = False, 0
    for it in range(1, max_iter + 1):
        f = np.array([o.value(x) for o in obs])
        r = (tgt - f) * 100.0
        z = r * np.sqrt(w) / sig
        hw = huber_weights(z, k)
        W = np.where(act, hw * w / sig ** 2, 0.0)
        J = jacobian(obs, x, f) * 100.0          # bp per percent
        A = np.vstack([np.sqrt(W)[:, None] * J, np.diag(100.0 / prior_sigma_bp)])
        b = np.concatenate([np.sqrt(W) * r, 100.0 * (prior - x) / prior_sigma_bp])
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
    # hat-matrix diagonal: rows a_i = sqrt(w_i)/sigma_i J_i against the final information matrix
    A = np.vstack([np.sqrt(W)[:, None] * J, np.diag(100.0 / prior_sigma_bp)])
    rows = (np.sqrt(w) / sig)[:, None] * J
    lev = np.einsum("ij,ij->i", rows @ np.linalg.pinv(A.T @ A), rows) * np.where(act, hw, 1.0)
    return x, f, r, hw, np.sqrt(W)[:, None] * J, lev, it, converged


def fit(obs: list[Observation], prior: np.ndarray, prior_sigma_bp: np.ndarray | float, *, huber_k: float = 1.345,
        drop_weight: float = 0.2, max_iter: int = 50, tol_bp: float = 1e-5, x0: np.ndarray | None = None) -> FitResult:
    prior = np.asarray(prior, dtype=float)
    ps = np.broadcast_to(np.asarray(prior_sigma_bp, dtype=float), prior.shape).copy()
    x = prior.copy() if x0 is None else np.asarray(x0, dtype=float).copy()
    active = list(range(len(obs)))
    dropped: list[int] = []
    rounds: list[list[int]] = []
    total_it = 0
    for _ in range(MAX_DROP_ROUNDS):
        x, f, r, hw, Jw, lev, it, conv = _solve(obs, active, x, prior, ps, huber_k, max_iter, tol_bp)
        total_it += it
        new = [i for i in active if hw[i] < drop_weight]
        if not new:
            break
        rounds.append(new)
        dropped += new
        active = [i for i in active if i not in new]
    lev = np.clip(lev, 0.0, 1.0)
    lev[dropped] = np.nan            # not part of the final problem
    return FitResult(x, f, r, hw, dropped, identification(Jw), lev, total_it, conv, rounds)
