"""Reproduce the decay experiment, figures, and convergence table."""
from pathlib import Path
import csv
import platform
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ode_methods import solve

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"

def main():
    RESULTS.mkdir(exist_ok=True)
    plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "axes.grid": False})
    rows = []
    for method in ("euler", "rk4"):
        previous = None
        for n in (10, 20, 40, 80, 160):
            t, y = solve(lambda t, y: -y, 1., 0., 2., n, method)
            error = float(np.max(np.abs(y - np.exp(-t))))
            order = "" if previous is None else np.log2(previous / error)
            rows.append([method, n, 2 / n, error, order])
            previous = error
    with (RESULTS / "python_convergence.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["method", "n_steps", "h", "max_error", "observed_order"])
        writer.writerows(rows)
    t, euler = solve(lambda t, y: -y, 1., 0., 2., 20, "euler")
    _, rk4 = solve(lambda t, y: -y, 1., 0., 2., 20, "rk4")
    np.savetxt(RESULTS / "python_trajectory.csv", np.column_stack((t, np.exp(-t), euler, rk4)), delimiter=",", header="t,exact,euler,rk4", comments="")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(t, np.exp(-t), "k-", label="Exact")
    ax.plot(t, euler, "o--", color="#7c3aed", label="Euler", markersize=3)
    ax.plot(t, rk4, "s:", color="#bd7200", label="RK4", markersize=3)
    ax.set(xlabel="Time t", ylabel="y(t)", title="Exponential decay: y' = -y, y(0) = 1; h = 0.1")
    ax.legend(); fig.tight_layout()
    fig.savefig(RESULTS / "solution.svg", metadata={"Date": None}); plt.close(fig)
    fig, ax = plt.subplots(figsize=(7, 4))
    for method, marker in (("euler", "o-"), ("rk4", "s--")):
        data = [r for r in rows if r[0] == method]
        ax.loglog([r[2] for r in data], [r[3] for r in data], marker, label=method.upper())
    ax.set(xlabel="Step size h", ylabel="Maximum nodal absolute error", title="Convergence against the exact solution")
    ax.legend(); fig.tight_layout()
    fig.savefig(RESULTS / "convergence.svg", metadata={"Date": None}); plt.close(fig)
    (RESULTS / "python_environment.txt").write_text(f"Python {platform.python_version()}\nNumPy {np.__version__}\nMatplotlib {matplotlib.__version__}\n")
    for row in rows:
        print(row)

if __name__ == "__main__":
    main()
