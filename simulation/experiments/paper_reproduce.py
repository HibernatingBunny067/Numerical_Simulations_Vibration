import numpy as np
from model import Parameters,resolver_nd
from simulation.runner import run_one
from simulation.storage import save_result
from simulation.features import extract_features
from tqdm import tqdm

def reproduce_paper(base:Parameters) -> None:
    sampled = base.sample("paper")
    params_nd,total_tau = resolver_nd(base,sampled)

    result = run_one(params_nd,total_tau)

    features = extract_features(result,True)

    params = {
        **sampled,
        **features,
        "Omega_bar":params_nd[1]
    }
    
    save_result(params,
                result,
                True,
                "paper_reproduction",
                "paper_meta_file.csv")
    
def omega_sweep(base:Parameters,n:int = 120):
    Omega_vals = np.linspace(0.5,1.5,n)
    ecc_vals = np.linspace(0.1,0.8,10)
    for Omega in tqdm(Omega_vals,desc="Sweeping OMEGA",leave=False):
        for e_bar in ecc_vals:
            sampled = base.sample("paper")

            sampled['f_shaft'] = Omega * base.f_n
            sampled['ecc'] = e_bar * base.clearance

            params_nd,total_tau = resolver_nd(base,sampled)

            result = run_one(params_nd,total_tau)

            features = extract_features(result)

            params = {
                **sampled,
                **features,
                "Omega_bar":Omega,
                "e_bar":e_bar
            }

            save_result(params=params,metafile_name="omega_sweep.csv")

if __name__ == "__main__":
    base = Parameters()

    reproduce_paper(base)
    omega_sweep(base,n=1000)
