# 1-DOF Numerical Simulations (Custom RK45)

Numba-accelerated adaptive RK45 (`Dormand–Prince 5(4)`) integrator plus a small simulation harness for a non-dimensional rotor/stator rubbing model aligned with `papers/main.pdf`.

## What’s in this repo

- **Core solver**: adaptive RK45 stepping + Hermite interpolation to a uniform grid.
- **Model**: non-dimensional state-space dynamics and a single “paper baseline” parameter set.
- **Simulation**: experiments (paper reproduction + parameter sweeps), feature extraction, and result storage.
- **Notebooks**: analysis/validation plots that reference specific figures in `papers/main.pdf`.

## Quick start

Create a virtualenv, install requirements, and run the baseline reproduction:

- `./run_simulations.sh`

Or, after installing dependencies yourself:

- `python3 -m simulation.main --reproduce-paper`

Run an Omega sweep:

- `python3 -m simulation.main --omega-sweep --n 500`

## Project structure

- `core/` — RK45 implementation
  - `core/integrator.py` (Numba RK45 stepper + adaptive loop)
  - `core/solver.py` (public `rk45` wrapper + sampling)
  - `core/sampling.py` (interpolation to `t_eval`)
- `model/` — dynamics + parameter mapping
  - `model/system.py` (system RHS: `f(t, state, params_nd)`)
  - `model/parameters.py` (dimensional parameters + `resolver_nd`)
- `simulation/` — experiments + storage
  - `simulation/main.py` (CLI entrypoint)
  - `simulation/experiments/paper_reproduce.py` (baseline + sweep)
  - `simulation/features.py` (steady-state feature extraction)
  - `simulation/storage.py` (raw `.npz` + metadata `.csv`)
- `notebooks/` — analysis and reporting
  - `notebooks/analysis.ipynb` (paper-aligned validation + sweep interpretation)
  - `notebooks/README.md` (what each notebook does)
- `benchmarking/` — quick comparison against SciPy’s `solve_ivp(RK45)`
- `papers/` — references (including `papers/main.pdf`)

## Outputs

By default results are written under `results/`:

- `results/raw/` — raw trajectories (`.npz`) when enabled by the experiment
- `results/metadata/` — run metadata + extracted features (`.csv`)

## API expectations

The solver expects a system function with signature:

- `f(t, state, params_nd) -> ndarray`

where `params_nd` is a NumPy array (see `model/system.py` and `model/parameters.py`).

## Next improvements (optional)

- [ ] Implement and surface solver **event detection** in `rk45Output`.
- [ ] Replace cubic Hermite sampling with native **Dormand–Prince dense output**.
