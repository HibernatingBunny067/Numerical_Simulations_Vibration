## Benchmarking

This folder contains quick benchmarks and checks comparing the custom RK45 solver (`core/solver.py`) against SciPy’s `solve_ivp(method="RK45")`.

### Scripts

- `quick_test.py`
  - Small single-problem comparison (forced damped oscillator).
  - Prints runtime + error metrics and plots trajectories.

- `testing.py`
  - Runs a small suite of ODE problems from `systems.py` across multiple `rtol` values.
  - Produces a JSON/CSV-style summary plus a markdown report with plots under `benchmarking/results/`.

- `systems.py`
  - Defines the benchmark ODE right-hand-sides in two forms:
    - pure-Python versions for SciPy
    - Numba-compiled versions for the custom solver (matching the required solver signature)

### Outputs

Running `testing.py` writes:

- `benchmarking/results/benchmark_results.json`
- `benchmarking/results/report.md`
- `benchmarking/results/figures/*.png`

These are generated artifacts and are typically not committed.

### Run

From the repo root (after installing requirements):

- `python3 benchmarking/quick_test.py`
- `python3 benchmarking/testing.py`

