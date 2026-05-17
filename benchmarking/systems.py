import numpy as np
from numba import njit

# constants used in the testing systems
LAMBDA = 0.5

OMEGA_N = 1.0
ZETA = 0.05

OMEGA, F0 = 0.6, 2

R, K = 0.01, 3

MU = 0.3


#pythonic for scipy
def exponential_system_py(t, state):
    x = state[0]
    return np.array([LAMBDA * x], dtype=np.float64)


def harmonic_oscillator_py(t, state):
    x, xdot = state
    return np.array([xdot, -OMEGA_N**2 * x], dtype=np.float64)


def damped_harmonic_oscillator_py(t, state):
    x, xdot = state
    return np.array([
        xdot,
        -2 * ZETA * OMEGA_N * xdot - OMEGA_N**2 * x
    ], dtype=np.float64)


def forced_oscillator_py(t, state):
    x, xdot = state
    return np.array([
        xdot,
        -OMEGA_N**2 * x + F0 * np.sin(OMEGA * t)
    ], dtype=np.float64)


def logistic_system_py(t, state):
    x = state[0]
    return np.array([R * x * (1 - x / K)], dtype=np.float64)


def van_der_pol_system_py(t, state):
    x, xdot = state
    return np.array([
        xdot,
        MU * (1 - x**2) * xdot - x
    ], dtype=np.float64)


# numba compiled for custom solver
@njit
def exponential_system(t, state, _params):
    x = state[0]
    out = np.empty(1)
    out[0] = LAMBDA * x
    return out


@njit
def harmonic_oscillator(t, state, _params):
    x = state[0]
    xdot = state[1]

    out = np.empty(2)
    out[0] = xdot
    out[1] = -OMEGA_N**2 * x
    return out


@njit
def damped_harmonic_oscillator(t, state, _params):
    x = state[0]
    xdot = state[1]

    out = np.empty(2)
    out[0] = xdot
    out[1] = -2 * ZETA * OMEGA_N * xdot - OMEGA_N**2 * x
    return out


@njit
def forced_oscillator(t, state, _params):
    x = state[0]
    xdot = state[1]

    out = np.empty(2)
    out[0] = xdot
    out[1] = -OMEGA_N**2 * x + F0 * np.sin(OMEGA * t)
    return out


@njit
def logistic_system(t, state, _params):
    x = state[0]

    out = np.empty(1)
    out[0] = R * x * (1 - x / K)
    return out


@njit
def van_der_pol_system(t, state, _params):
    x = state[0]
    xdot = state[1]

    out = np.empty(2)
    out[0] = xdot
    out[1] = MU * (1 - x**2) * xdot - x
    return out


## exported problems
problems_py = [
    exponential_system_py,
    harmonic_oscillator_py,
    damped_harmonic_oscillator_py,
    forced_oscillator_py,
    logistic_system_py,
    van_der_pol_system_py
]

problems_njit = [
    exponential_system,
    harmonic_oscillator,
    damped_harmonic_oscillator,
    forced_oscillator,
    logistic_system,
    van_der_pol_system
]
