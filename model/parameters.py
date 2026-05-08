from dataclasses import dataclass,field
import numpy as np
from numpy.typing import NDArray
from typing import Dict,Literal,Tuple

@dataclass(frozen=True)
class univIndex:
    '''
    Universal params array index, used globally in the project.
    '''
    idx:Dict[str,int] = field(default_factory= lambda: {
        "ZETA":0,
        "OMEGA_BAR":1,
        "E_BAR":2,
        "KC_BAR":3,
        "MU":4,
        "R_DISK_BAR":5
    })


np.random.seed(42) ##for reproducibility
@dataclass(frozen = True)
class Parameters:
    '''
    Dimensional parameter values later resolved to non dimensional, dynamically at runtime
    '''
    m:float = 1.0                  #kg
    f_n:float = 50.0               # Hertz
    zeta:float = 0.05              
    clearance:float = 1e-3          #m or 1mm 
    r_disk:float = 0.05            #m or 5 cm


    # rotor physics
    eccentricity:NDArray = field(default_factory=lambda: np.array([1e-5,5e-4])) #m
    f_shaft:NDArray = field(default_factory=lambda: np.array([10, 150]))  # Hertz

    # rub-impact physics
    kc:NDArray = field(default_factory=lambda: np.array([1e5, 1e7]))   # N/m
    mu:NDArray = field(default_factory=lambda: np.array([0.0, 0.2]))


    # simulation
    T_total:float = 1.0           #seconds

    def __post_init__(self):
        omega_n = 2 * np.pi * self.f_n
        object.__setattr__(self, "omega_n", omega_n)                    #rad/s
        object.__setattr__(self, "k", self.m * omega_n**2)              # N/m
        object.__setattr__(self, "c", 2 * self.zeta * self.m * omega_n) # Ns/m^2

    def sample(self,
               mode:Literal["sampled","paper"] = "sampled") -> Dict:
        '''
        returns dimensional sampled parameters
        '''
        if mode == "sampled":
            return {
            "f_shaft": np.random.uniform(*self.f_shaft),
            "ecc": np.random.uniform(*self.eccentricity),
            "kc": np.random.uniform(*self.kc),
            "mu": np.random.uniform(*self.mu),
            }
        if mode == "paper":
            return self.from_paper()
        
        print("Select correct sampling method and retry") 
    
    def from_paper(self) -> Dict:
        '''
        return dimensional parameters taken from the paper "./papers/main.pdf - Page 15"
        '''
        return {
            "f_shaft": self.f_n,
            "ecc": 0.5*self.clearance,
            "kc": 7*self.k,   #type: ignore
            "mu": 0.01,
            "r_disk": 10.0
        }

def resolver_nd(base:Parameters,sampled:Dict) -> Tuple[NDArray,float]:
    '''
    Takes the dimensional parameters (sampled or directly from paper),
    and returns the non-dimensional parameters in a numpy array indexed by the universal scheme defined at the top of this file.
    '''
    omega = 2*np.pi*sampled["f_shaft"]
    Omega_bar = omega / base.omega_n                        #type:ignore

    e_bar = sampled.get("ecc",0.1) / base.clearance

    kc_bar = sampled.get("kc") /base.k                      #type:ignore
    r_disk_bar = sampled.get("r_disk",base.r_disk) / base.clearance

    total_tau = base.T_total * base.omega_n                 #type:ignore
    
    return np.array([
        base.zeta,
        Omega_bar,
        e_bar,
        kc_bar,
        sampled.get("mu",0.01),
        r_disk_bar
    ],dtype=np.float64), total_tau


