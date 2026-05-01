import numpy as np
from numpy.typing import NDArray
from numba import njit

@njit
def imbalance_force(t:float,params:NDArray) -> float:
    return (params[6]/params[0]) * np.sin(params[5]*t)

@njit
def fault_force(t:float,params:NDArray) -> float:
    '''
    This essentially runs for each RK45 step, which can become computationally very expensive for large time simulations
    We'll cap the N based on the value of t and T_f
    '''
    total:float = 0.0
    N:int = int(t / params[8])

    for n in range(max(0,N-5),N+1):
        tau = t - n*params[8]
        if tau > 0:
            total += params[9] * np.exp(-params[3] * tau)*np.sin(params[1]*tau)

    return total / params[0]

@njit
def system(t:float,state:NDArray,params:NDArray) -> tuple:
    x,xdot = state

    xddot = (
        -2 * params[2] * params[1] * xdot
        - params[1]**2 * x
        + imbalance_force(t,params)
        + fault_force(t,params)
    )
    return (xdot,xddot)