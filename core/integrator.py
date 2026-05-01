from numba import njit
import numpy as np
from numpy.typing import NDArray
from typing import Callable,Tuple


ctab = np.array([0,1/5,3/10,4/5,8/9,1,1],dtype = np.float64)
b5 = np.array([35/384, 0, 500/1113, 125/192, -2187/6784, 11/84, 0],dtype = np.float64)
b4 = np.array([5179/57600, 0, 7571/16695, 393/640, -92097/339200, 187/2100, 1/40],dtype = np.float64)
atab = np.array([
    [0, 0, 0, 0, 0, 0],
    [1/5, 0, 0, 0, 0, 0],
    [3/40, 9/40, 0, 0, 0, 0],
    [44/45, -56/15, 32/9,0,0,0],
    [19372/6561, -25360/2187, 64448/6561, -212/729, 0, 0],
    [9017/3168, -355/33, 46732/5247, 49/176, -5103/18656, 0],
    [35/384, 0, 500/1113, 125/192, -2187/6784, 11/84]
    ],dtype = np.float64)

@njit
def rk45_step(
    t:float, 
    y:NDArray, 
    h:float, 
    rtol:float, 
    atol:float, 
    system:Callable, 
    kstages:NDArray,
    sum_term:NDArray,
    y5:NDArray,
    y4:NDArray
) -> Tuple[NDArray,NDArray]:
    state_dim = y.shape[0]
    for i in range(1,7):
        sum_term[:] = 0
        for j in range(i):
            for k in range(state_dim):
                sum_term[k] += atab[i, j] * kstages[j,k]
        y_temp = y + h * sum_term
        t_temp = t + ctab[i] * h
        kstages[i] = system(t_temp, y_temp)

    y5[:] = y
    y4[:] = y
    for i in range(7):
        y5 += h * b5[i] * kstages[i]
        y4 += h * b4[i] * kstages[i]

    scale = np.empty_like(y)
    for i in range(y.shape[0]):
        a = abs(y[i])
        b = abs(y5[i])
        if a > b:
            scale[i] = atol + rtol * a
        else:
            scale[i] = atol + rtol * b
    err_sum = 0.0

    for k in range(state_dim):
        val = (y5[k]-y4[k]) / scale[k]
        err_sum += val*val

    err = np.sqrt(err_sum / state_dim) + 1e-14

    return y5.copy(),err


@njit 
def integrate_core(
    t0:float,
    tf:float,
    y0:NDArray,
    h0:float,
    max_steps:int,
    rtol:float,
    atol:float,
    system:Callable,
) -> tuple[NDArray,NDArray,NDArray]:
    t = t0
    state_dim = y0.shape[0]
    y:NDArray = np.empty(state_dim)

    y[:] = y0
    h = h0
    
    y4,y5 = np.empty_like(y),np.empty_like(y)
    ts = np.empty(max_steps)
    ys = np.empty((max_steps, state_dim))
    fs = np.empty((max_steps, state_dim))

    idx = 0

    ts[idx] = t
    ys[idx] = y
    fs[idx] = system(t, y)
    kstages = np.empty((7,state_dim))
    sum_term = np.empty_like(y)
    kstages[0] = system(t,y0)
    while t < tf:

        h = min(h, tf - t)

        y_new, error = rk45_step(
            t,
            y,
            h,
            rtol,
            atol,
            system,
            kstages,
            sum_term,
            y5,y4
        )

        if error < 1.0:
            t += h
            y = y_new
            kstages[0] = kstages[6]

            idx += 1

            if idx >= max_steps:
                raise RuntimeError("Exceeded storage")

            ts[idx] = t
            ys[idx] = y
            fs[idx] = kstages[6]

        if error == 0.0:
            s = 2.0
        else:
            s = 0.9 * (1.0 / error)**0.2

        if s < 0.2:
            s = 0.2
        elif s > 2.0:
            s = 2.0

        h = h * s

        if h < 1e-8:
            raise RuntimeError("Step size too small")

    return (
        ts[:idx+1],
        ys[:idx+1],
        fs[:idx+1]
    )