"""Robust IRLS with the step prior on constructed problems (D4)."""
import numpy as np

from stircurve.curves import robust


def _linear_obs(A, y, sigma=0.5, w=None):
    w = np.ones(len(y)) if w is None else w
    return [robust.Observation(f"q{i}", (lambda x, a=a: float(a @ x)), float(t), sigma, float(wi))
            for i, (a, t, wi) in enumerate(zip(A, y, w))]


def test_over_identified_fit_recovers_the_truth_and_ignores_the_weak_prior():
    rng = np.random.default_rng(0)
    truth = np.array([4.0, 4.25, 4.5, 4.5, 4.75])
    A = np.vstack([np.eye(5), np.eye(5), 0.5 * (np.eye(5) + np.roll(np.eye(5), 1, axis=1))])
    y = A @ truth
    prior = robust.Prior.steps(5, 100.0, 4.0, 25.0)
    res = robust.fit(_linear_obs(A, y), prior, np.full(5, 4.0))
    assert res.converged and np.max(np.abs(res.x - truth)) * 100 < 0.05       # the prior's pull is well under 0.05bp
    assert np.all(res.identification > 0.99) and not res.dropped
    assert np.all(res.posterior_sigma_bp < 0.5)


def test_huber_caps_one_bad_quote_and_the_drop_list_names_it():
    truth = np.array([4.0, 4.25, 4.5])
    A = np.vstack([np.eye(3), np.eye(3), np.eye(3)])
    y = A @ truth
    y[4] += 0.05                                                 # 5bp off on one copy of parcel 1
    prior = robust.Prior.steps(3, 100.0, 4.0, 25.0)
    res = robust.fit(_linear_obs(A, y), prior, np.full(3, 4.0), huber_k=1.345, drop_weight=0.2)
    assert res.dropped == [4] and np.max(np.abs(res.x - truth)) * 100 < 0.05
    assert abs(res.residual_bp[4] - 5.0) < 0.05


def test_leverage_one_quote_is_invisible_to_residuals_but_not_to_leave_one_out():
    """Parcel 2 is pinned by one quote only: an error in it moves the parcel; the LOO residual sees it."""
    truth = np.array([4.0, 4.25, 4.5])
    A = np.array([[1, 0, 0], [1, 0, 0], [0, 1, 0], [0, 1, 0], [0, 0, 1.0]])
    y = A @ truth
    y[4] += 0.05
    prior = robust.Prior.steps(3, 100.0, 4.0, 25.0)
    obs = _linear_obs(A, y)
    res = robust.fit(obs, prior, np.full(3, 4.0))
    assert res.leverage[4] > 0.95 and abs(res.residual_bp[4]) < 0.2 and not res.dropped
    loo = robust.leave_one_out(obs, prior, res)
    assert loo[4] > 4.0                                          # with the quote out, the step prior keeps parcel 2 near parcel 1


def test_under_identified_parcels_take_the_equal_step_split():
    """One quote prices the average of parcels 1-3 (three meetings inside one OIS): with the ties the prior
    splits the change equally; without them the ridge front-loads it (later steps touch fewer days)."""
    A = np.array([[1, 0, 0, 0], [0, 1 / 3, 1 / 3, 1 / 3]])
    y = np.array([4.0, 4.5])
    tied = robust.Prior.steps(4, 100.0, 4.0, 25.0, ties=[(1, 2), (2, 3)], tie_tau_bp=2.0)
    res = robust.fit(_linear_obs(A, y), tied, np.full(4, 4.0))
    steps = np.diff(res.x)
    assert abs(res.x[1:].mean() - 4.5) < 1e-4 and np.allclose(steps, steps[0], rtol=0.01) and steps[0] > 0
    assert res.identification[0] > 0.99 and np.all(res.identification[1:] < 0.99)
    loose = robust.fit(_linear_obs(A, y), robust.Prior.steps(4, 100.0, 4.0, 25.0), np.full(4, 4.0))
    s2 = np.diff(loose.x)
    assert s2[0] > s2[1] > s2[2] > 0


def test_steps_beyond_the_data_are_flat():
    A = np.array([[1, 0, 0, 0], [0, 1, 0, 0.0]])
    y = np.array([4.0, 4.5])
    prior = robust.Prior.steps(4, 100.0, 4.0, 25.0, beyond_from=2, beyond_tau_bp=0.5)
    res = robust.fit(_linear_obs(A, y), prior, np.full(4, 4.0))
    assert np.allclose(res.x, [4.0, 4.5, 4.5, 4.5], atol=1e-6)


def test_weights_scale_the_quote_noise():
    truth = np.array([4.0, 4.5])
    A = np.array([[1, 0], [0, 1], [0, 1.0]])
    y = A @ truth
    y[2] += 0.04                                                 # a thin quote 4bp off
    prior = robust.Prior.steps(2, 100.0, 4.0, 25.0)
    heavy = robust.fit(_linear_obs(A, y, w=np.array([1, 1, 1.0])), prior, truth, huber_k=10)
    light = robust.fit(_linear_obs(A, y, w=np.array([1, 1, 0.05])), prior, truth, huber_k=10)
    assert abs(heavy.x[1] - 4.52) < 1e-3 and abs(light.x[1] - truth[1]) * 100 < 0.3
