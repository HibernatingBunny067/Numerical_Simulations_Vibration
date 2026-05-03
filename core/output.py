from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray

@dataclass
class rk45Output:
    '''
    This is directly taken from scipy.integrate.solve_vip implementation.
    The result there is wrapped in an output object instead of bare dictionaries
    '''
    t:NDArray
    y:NDArray ##Scipy follows (state_dim,N) we follow (N,state_dim)
    n_steps: int
    predicted_n: int
    status: int
    message: str

    def __repr__(self) -> str:
        return (
            f"RK45 Result(status = {self.status}), "
            f"Steps: {self.n_steps}, "
            f"Predicted n: {self.predicted_n}, "
            f"T-Span: ({self.t[0]:.3f},{self.t[-1]:.3f})"
        )