from numpy.typing import NDArray
from typing import Dict
import numpy as np
from core import rk45
from model import system

def run_one(params_nd:NDArray,total_tau:float) -> Dict:
    y0 = np.array([0.01,0.0,0.0,0.0],dtype=np.float64)
    t_uniform = np.linspace(0,total_tau,2000)
    sol = rk45(
        system,
        y0,
        np.array([0,total_tau]),
        t_eval=t_uniform,
        sys_params=params_nd
    )

    return {
        "t":sol.t,
        "y":sol.y
    }
