import warnings
warnings.filterwarnings("ignore")
from experiments.omega_sweep import run_omega_sweep




# Simulation strtegy
# - First we simulate the system as mentioned in paper 
# - After that we sweep over Omega values (from 0.9 to 1.5) to cover sub-critical, critical and over-critical regimes
# - In each sweep we sample other parameters and simulate the system
# - Raw time series is stored as .npz files and metadata for each file will be store in a .csv file


run_omega_sweep(n = 20)