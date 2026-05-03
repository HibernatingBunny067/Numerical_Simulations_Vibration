import numpy as np
import sys
sys.path.append(r'/Users/harikesh/Documents/Numerical Simulations/1-DOF_Project')
from model import Parameters,resolver_nd
from simulation.runner import run_one
from simulation.storage import save_result
from tqdm import tqdm
from features import extract_features

def run_omega_sweep(n = 40):
    base = Parameters()

    Omega_vals = np.linspace(0.9,1.5,n)

    for Omega in tqdm(Omega_vals,leave=False):
        sampled = base.sample(mode='paper')
        sampled['f_shaft'] = Omega * base.f_n
        sampled['ecc'] = 0.05
        params_nd,total_tau = resolver_nd(base,sampled)

        result = run_one(params_nd,total_tau)

        features = extract_features(result)

        params = {
            **sampled,
            **features,
            "Omega_bar":Omega
        }


        save_result(result,params)
