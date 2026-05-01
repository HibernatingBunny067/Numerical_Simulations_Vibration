from core.solver import rk45
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from numba import njit
import numpy as np
import time
import math

zeta = 0.05
omega_n = 1.0


def system_scipy(t, state):
    x, v = state

    xddot = (
        -2*zeta*omega_n*v
        -omega_n**2*x
        + math.sin(20*t)
    )

    return np.array([v, xddot])


@njit
def system_custom(t, state):
    x, v = state

    xddot = (
        -2*zeta*omega_n*v
        -omega_n**2*x
        + np.sin(20*t)
    )

    return np.array([v, xddot])


if __name__ == "__main__":

    t_span = [0, 10.0]
    y0 = [1.0, 0.0]

    t_uniform = np.linspace(0, 10.0, 250)

    wd = omega_n * np.sqrt(1 - zeta**2)

    A = 1.0
    B = (zeta * omega_n) / wd

    x_true = np.exp(-zeta*omega_n*t_uniform) * (
        A*np.cos(wd*t_uniform) +
        B*np.sin(wd*t_uniform)
    )

    solution = rk45(
        f = system_custom,
        y0=y0,
        t_span=t_span,
        h0=None,
        n = len(t_uniform)
    )
    start = time.perf_counter()
    solution = rk45(
        f = system_custom,
        y0=y0,
        t_span=t_span,
        h0=None,
        n = len(t_uniform)
    )
    custom_time = time.perf_counter() - start

    start = time.perf_counter()
    scipy_sol = solve_ivp(
        system_scipy,
        t_span,
        y0,
        method="RK45",
        t_eval=t_uniform,
        rtol=1e-6,
        atol=1e-9
    )
    scipy_time = time.perf_counter() - start
    t_custom = solution["t"]
    y_custom = solution["y"]
    custom_error = np.max(np.abs(x_true - y_custom[:, 0]))
    scipy_error = np.max(np.abs(x_true - scipy_sol.y[0]))

    custom_vs_scipy = np.max(
        np.abs(y_custom[:, 0] - scipy_sol.y[0])
    )

    print("\n----- Performance -----")
    print(f"Custom Solver Time: {custom_time:.6f}s")
    print(f"SciPy Solver Time:  {scipy_time:.6f}s")

    print("\n----- Accuracy -----")
    print(f"Custom vs Analytical: {custom_error:.2e}")
    print(f"SciPy vs Analytical:  {scipy_error:.2e}")
    print(f"Custom vs SciPy:      {custom_vs_scipy:.2e}")

    print("\n----- Internal Solver Stats -----")
    print("SciPy nfev:", scipy_sol.nfev)
    print("Custom solver: ", solution["n"])
    plt.figure(figsize=(12,6))

    plt.plot(
        t_custom,
        y_custom[:,0],
        'ro--',
        label="Custom Solver"
    )

    plt.plot(
        scipy_sol.t,
        scipy_sol.y[0],
        'b',
        label="SciPy RK45"
    )

    plt.plot(
        t_uniform,
        x_true,
        'g',
        alpha=0.7,
        label="Analytical"
    )

    plt.legend()
    plt.grid()
    plt.title("Custom RK45 vs SciPy RK45 vs Analytical")
    plt.show()