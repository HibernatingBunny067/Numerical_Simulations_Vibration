## Notebooks

This directory contains exploratory and reporting notebooks for the project.

- `analysis.ipynb`: Paper-aligned validation + parameter-sweep analysis against `../papers/main.pdf`.
- `Simulation.ipynb`: Ad-hoc simulation exploration (workbench-style).

### analysis.ipynb: what it shows

The notebook is structured to validate the key qualitative behaviors reported in `../papers/main.pdf` and to summarize them over a controlled sweep in non-dimensional speed.

**Baseline (paper reproduction) figures**

1. **Orbit radius history `R(τ)` vs `τ`**
   - Interpretation: transient build-up near resonance; saturation once the clearance boundary is reached and rubbing/constraint activates.
   - Paper cross-check: `../papers/main.pdf` **Fig. 12** (PDF p. 9) compares non-dimensional amplitude with/without rub-impact.

2. **Phase portrait / orbit (`X` vs `Y`) with clearance circle**
   - Interpretation: transition from near-circular free whirl to a distorted/clearance-limited orbit once rubbing engages.
   - Paper cross-check: `../papers/main.pdf` **Fig. 13** (PDF p. 10) shows orbits + constraint stiffness vs speed ratio; **Fig. 17** (PDF p. 12) shows experimentally measured rubbing-state orbits.

3. **Penetration and contact state vs `τ`**
   - Interpretation: penetration `max(R-1,0)` and binary contact `(R>1)` are direct measures of rubbing engagement and intermittency.
   - Paper cross-check: `../papers/main.pdf` **Fig. 13** (PDF p. 10) links orbit changes with constraint stiffness/contact evolution.

**Omega sweep figures**

4. **Sweep summary (1×3): `R_mean`, `R_std`, mean penetration vs `Ω̄` (colored by `e_bar`)**
   - Interpretation:
     - `R_mean` indicates how close the steady-state orbit is to clearance.
     - `R_std` highlights variability/intermittency (often strongest near `Ω̄≈1` and under contact).
     - mean penetration is a direct “contact severity” proxy.
   - Paper cross-check: `../papers/main.pdf` **Fig. 12** (PDF p. 9) and **Fig. 19** (PDF p. 13) show amplitude–speed trends and how constraint state changes them.

5. **Spectral summary (2×2): dominant freq/amp in `X` and `Y` vs `Ω̄` (colored by `e_bar`)**
   - Interpretation:
     - Dominant frequency/amp summarize the strongest steady-state component in each channel.
     - Increased scatter or shifts with `Ω̄` can indicate non-smooth contact, harmonics, and instability regions.
   - Paper cross-check: `../papers/main.pdf` **Fig. 7** (PDF p. 6) Campbell diagram (frequency vs speed) and **Fig. 8** (PDF p. 7) stiffness influence on modal frequencies.

### Inputs / reproducibility

`analysis.ipynb` can load inputs either from `.env` variables or from defaults under `../results/` (see the “Inputs” cell inside the notebook).

