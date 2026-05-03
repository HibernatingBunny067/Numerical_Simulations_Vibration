# Simulation Strategy:

1. Baseline Validation:
   - Simulate the system using parameters directly from the paper.
   - Verify phase portrait, orbit radius, and contact behavior.

2. Controlled Frequency Sweep:
   - Sweep Ω ∈ [0.9, 1.5] to cover:
       • sub-critical (Ω < 1)
       • near-critical (Ω ≈ 1)
       • super-critical (Ω > 1)

3. Parameter Control:
   - Keep all other parameters fixed initially.
   - Perform separate controlled sweeps for:
       • μ (friction)
       • k_c_bar (contact stiffness)
       • e_bar (eccentricity)

4. Simulation Output:
   - Store raw time series (t, X, Y) as .npz
   - Store metadata + extracted features in .csv

5. Feature Extraction (steady-state only):
   - Mean orbit radius
   - Radius standard deviation
   - Contact ratio (R > 1)
   - Dominant Frequency (Fast-Fourier Transform)
   
6. Transient Removal:
   - Discard first 30–50% of simulation before analysis