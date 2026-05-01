from dataclasses import dataclass,field
import numpy as np
from typing import List
np.random.seed(42)

@dataclass(frozen = True)
class parameters():
    '''
    This class contains the global parameters to be swept upon,
    we'll use this as a base class to get our once fixed parameter ranges and values, 
    another similar class with scalar values will be used for runtime parameter allocation
    '''
    m:float = 1.0 ##mass of the system
    f_n:float = 300 #hertz ##natural frequency of the system
    zeta:float = 0.02 #damping coefficient

    f_shaft:np.ndarray = field(default_factory = lambda: np.array([10,150]))
    F0:np.ndarray = field(default_factory = lambda: np.array([1,50]))

    f_fault_multipliers:np.ndarray = field(default_factory = lambda: np.array([2,12]))
    A_base:np.ndarray = field(default_factory = lambda: np.array([10,120]))
    severity:np.ndarray = field(default_factory = lambda: np.array([0.1,1.0]))
    sigma:np.ndarray = field(default_factory = lambda: np.array([0.2,1.0]))

    dt: float = 1e-4
    T_total:float = 2.0

    PARAM_ORDER:List = field(default_factory=lambda :[
        "m",
        "omega_n",
        "zeta",
        "beta",
        "f_shaft",
        "omega",
        "F0",
        "f_fault",
        "T_f",
        "A"
    ])


    def __post_init__(self):
        object.__setattr__(self,"omega_n",2*np.pi*self.f_n)
        object.__setattr__(self,"k",2*self.m*self.omega_n**2)
        object.__setattr__(self,"c",2*self.zeta*self.omega_n)
        object.__setattr__(self,"beta",self.zeta*self.omega_n)


    def sample(self):
        return {
            "f_shaft": np.random.uniform(*self.f_shaft),
            "F0": np.random.uniform(*self.F0),
            "fault_multi":np.random.uniform(*self.f_fault_multipliers),
            "A_base":np.random.uniform(*self.A_base),
            "severity":np.random.uniform(*self.severity)**2,
        }





def resolver(
        base:parameters,
        f_shaft,
        F0,
        fault_multi,
        A_base,
        severity
    ):
    '''
    Inside the simulation sweep loop, this function will be called to return the 
    params as a numpy array.
    '''
    f_fault = fault_multi * f_shaft

    return np.array([
        base.m,
        base.omega_n,
        base.zeta,
        base.beta,
        f_shaft,
        2*np.pi*f_shaft,
        F0,
        f_fault,
        1 / f_fault,
        A_base*severity,
    ])
