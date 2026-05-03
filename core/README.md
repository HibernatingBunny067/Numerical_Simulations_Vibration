# <div align = "center">Dormand - Prince Adaptive RK45 using NumPy and Numba <div>

## Overview
- Implementation of an adaptive Runge-Kutta 4(5) solver using Dormand-Prince method, optimized with NumPy and Numba for performance.
## Structure
``` text
core/
├── integrator.py   # Numba-compiled kernel for RK45 step (Dormand–Prince tableau)
├── solver.py       # Adaptive RK45 wrapper + step control logic
└── sampling.py     # Post-processing via cubic Hermite interpolation
```

## Components

```integrator.py```
- Implements the core RK45 step algorithm (iteratively). 
- Uses Dormand-Prince coefficients
- JIT-compiled used Numba and NumPy

```solver.py```
- Handles adaptive step sizing
- Error estimation and control
- Act as a thin main interface for integration

```sampling.py```
- Provide (approx) dense outputs
- Currently uses Cubic Hermite Spline interpolation (```scipy.interpolate```)

### For benchmarking against ```scipy.integrate.solve_ivp``` look in the ```benchmaring``` folder in the project and search for ```report.md``` in the ```results``` subfolder

## Future Improvements (potentially)
- Dense output using Native Dormand-Price interpolation.
- Support for stiff systems