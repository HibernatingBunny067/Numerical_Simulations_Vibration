import numpy as np
from numba import njit
from numpy.typing import NDArray

'''
As numba doesn't work with python dictionaries, we convert the parameter object into a numpy array and define a universal indexing scheme to take out the respective parameters from the array
'''

#universal indexing scheme for the parameters 
ZETA, OMEGA_BAR, E_BAR, KC_BAR, MU, R_DISK_BAR = range(6)

@njit
def system(t: float, state: NDArray, params: NDArray) -> NDArray:

    X = state[0]
    Y = state[1]
    Xdot = state[2]
    Ydot = state[3]

    zeta = params[ZETA]
    Omega = params[OMEGA_BAR]
    e_bar = params[E_BAR]
    kc_bar = params[KC_BAR]
    Mu = params[MU]
    r_disk_bar = params[R_DISK_BAR]

    R = np.sqrt(X*X + Y*Y)

    # forcing
    Fx = e_bar * Omega * Omega * np.cos(Omega * t)
    Fy = e_bar * Omega * Omega * np.sin(Omega * t)

    # base dynamics
    F_x_total = Fx - 2*zeta*Xdot - X
    F_y_total = Fy - 2*zeta*Ydot - Y

    if R > 1.0:

        # v_center = Xdot*tx + Ydot*ty ## approximate 
        v_center = (Ydot*X - Xdot*Y)/(R*R + 1e-8) ##derivative of arctan(Y/X)
        v_spin = Omega * r_disk_bar
        v_t = R*v_center + v_spin

        s = np.sign(v_t)

        scale = kc_bar * (1.0 - 1.0 / R)

        Fx_rub = scale * (X - Mu * s * Y)
        Fy_rub = scale * (Y + Mu * s * X)

        F_x_total -= Fx_rub
        F_y_total -= Fy_rub

    out = np.empty(4)
    out[0] = Xdot
    out[1] = Ydot
    out[2] = F_x_total
    out[3] = F_y_total

    return out    
