"""Run after both implementations to check numerical agreement."""
from pathlib import Path
import csv
import numpy as np
root = Path(__file__).resolve().parents[1] / "results"
for name in ("trajectory", "convergence"):
    if not (root / f"matlab_{name}.csv").exists():
        raise SystemExit("Run matlab/run_experiment.m first; MATLAB results are missing.")
a = np.loadtxt(root / "python_trajectory.csv", delimiter=",", skiprows=1)
b = np.loadtxt(root / "matlab_trajectory.csv", delimiter=",", skiprows=1)
np.testing.assert_allclose(a, b, rtol=1e-11, atol=1e-13)
def read(language):
    with (root / f"{language}_convergence.csv").open() as f:
        return list(csv.DictReader(f))
for a, b in zip(read("python"), read("matlab"), strict=True):
    assert (a["method"], a["n_steps"]) == (b["method"], b["n_steps"])
    np.testing.assert_allclose(float(a["max_error"]), float(b["max_error"]), rtol=1e-5, atol=1e-14)
print("Python and MATLAB trajectories and errors agree within stated tolerances.")
