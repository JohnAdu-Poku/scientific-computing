"""Fixed-step methods for scalar initial-value problems."""
import numpy as np


def solve(rhs, y0, t0, t_end, n_steps, method="rk4"):
    """Return t, y on n_steps equal intervals; rhs(t, y) is scalar."""
    if isinstance(n_steps, bool) or not isinstance(n_steps, (int, np.integer)) or n_steps < 1:
        raise ValueError("n_steps must be a positive integer")
    if not np.isfinite([y0, t0, t_end]).all() or t_end <= t0:
        raise ValueError("Use finite inputs with t_end > t0")
    if method not in ("euler", "rk4"):
        raise ValueError("method must be euler or rk4")
    t = np.linspace(t0, t_end, n_steps + 1)
    h = (t_end - t0) / n_steps
    y = np.empty(n_steps + 1)
    y[0] = y0
    for j in range(n_steps):
        k1 = rhs(t[j], y[j])
        if method == "euler":
            y[j + 1] = y[j] + h * k1
        else:
            k2 = rhs(t[j] + h / 2, y[j] + h * k1 / 2)
            k3 = rhs(t[j] + h / 2, y[j] + h * k2 / 2)
            k4 = rhs(t[j] + h, y[j] + h * k3)
            y[j + 1] = y[j] + h * (k1 + 2*k2 + 2*k3 + k4) / 6
    return t, y
