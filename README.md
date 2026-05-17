## 1-DOF Numerical Simulations (Custom RK45)

This project contains a custom adaptive RK45 integrator (Numba-accelerated) and a small simulation harness for running parameterized experiments and saving results/metadata.

### Quick start

- Create env + install deps: `./run_simulations.sh`
- Or run directly (after installing deps): `python3 -m simulation.main`

By default, `simulation.main` runs the baseline paper reproduction run.

### CLI

`python3 -m simulation.main --help`

Examples:
- `python3 -m simulation.main --reproduce-paper`
- `python3 -m simulation.main --omega-sweep --n 500`

### Project layout

- `core/` RK45 implementation (`core/solver.py`, `core/integrator.py`)
- `model/` system dynamics and parameter mapping (`model/system.py`, `model/parameters.py`)
- `simulation/` experiment scripts, feature extraction, and storage
- `benchmarking/` quick comparison against SciPy RK45

### Outputs

Results are written under `results/`:
- `results/raw/` time series `.npz` (optional)
- `results/metadata/` metadata/features `.csv`

### Notes

- The integrator expects the system signature `f(t, state, params_nd)` where `params_nd` is a NumPy array (see `model/system.py`).

### Suggested further addition
- [] Implement Event detection in the solver
- [] Use Dormand-Prince interpolation instead of Cubic Spline in solver post-processing.
