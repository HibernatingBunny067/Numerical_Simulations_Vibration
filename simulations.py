from core import rk45
from models import parameters, resolver, system
import os
import numpy as np
from tqdm import tqdm


def run_parameter_sweep(base,n_samples=1000, initial_state=[0.0, 0.0]):
    failed:int = 0
    for idx in tqdm(range(n_samples),leave=False):
        params = base.sample()

        try:
            params_array = resolver(base,
                                    params['f_shaft'],
                                    params['F0'],
                                    params['fault_multi'],
                                    params["A_base"],
                                    params['severity'])
            

            solver = RK45(
                system,
                initial_state,
                [0, base.T_total],
                params_array
            )

            ts, ys = solver.integrate()

            filepath = f"./data/raw_npz/sim_{idx:05d}.npz"

            np.savez_compressed(
                filepath,
                ts = ts,
                ys = ys,
                params = params_array
            )

        except (ValueError, RuntimeError):
            print(f"Failed for sample {idx}")
            failed += 1
    print(f"Total succesfull simulation: {n_samples - failed}")
    print(f"Total failed simulations: {failed}")



if __name__ == "__main__":
    os.makedirs("./data/raw_npz",exist_ok=True)
    base = parameters()
    run_parameter_sweep(base)