import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time import perf_counter_ns
import sys
path = r'/Users/harikesh/Documents/Numerical Simulations/1-DOF_Project'
sys.path.append(path)
from scipy.integrate import solve_ivp
from core import rk45
from systems import problems_njit, problems_py


os.makedirs("./benchmarking/results", exist_ok=True)
os.makedirs("./benchmarking/results/figures",exist_ok=True)

Y0 = [
    np.array([0.0]),
    np.array([0.0, 1.0]),
    np.array([0.0, 1.0]),
    np.array([0.0, 0.0]),
    np.array([1.0]),
    np.array([0.0, 1.0])
]

rtol_list = [1e-3, 1e-6, 1e-7]
t_span = [0.0, 10.0]
t_eval = np.linspace(t_span[0], t_span[1], 1000)

results = []

# -------------------------------
# Helper
# -------------------------------
def safe_name(name: str) -> str:
    return name.replace(" ", "_")


# ===============================
# MAIN LOOP
# ===============================
for f_py, f_njit, y0_vec in zip(problems_py, problems_njit, Y0):
    problem_name = " ".join(f_py.__name__.split('_')[:-2])
    safe_problem = safe_name(problem_name)

    print(f"\nRunning: {problem_name}")

    rk45(f=f_njit, y0=y0_vec, t_span=t_span, t_eval=t_eval)

    for rtol in rtol_list:

        t1 = perf_counter_ns()
        sol_custom = rk45(
            f=f_njit,
            y0=y0_vec,
            t_span=t_span,
            t_eval=t_eval,
            rtol=rtol
        )
        t2 = perf_counter_ns()

        t3 = perf_counter_ns()
        sol_scipy = solve_ivp(
            fun=f_py,
            t_span=t_span,
            y0=y0_vec,
            method="RK45",
            t_eval=t_eval,
            rtol=rtol,
            atol=1e-9
        )
        t4 = perf_counter_ns()

        y_custom = sol_custom["y"]
        y_scipy = sol_scipy.y.T

        diff = y_custom - y_scipy

        results.append({
            "problem": problem_name,
            "safe_name": safe_problem,
            "rtol": rtol,
            "custom_time_ns": int(t2 - t1),
            "scipy_time_ns": int(t4 - t3),
            "custom_steps": int(len(sol_custom["t"])),
            "scipy_steps": int(len(sol_scipy.t)),
            "l2_error": float(np.linalg.norm(diff)),
            "max_error": float(np.max(np.abs(diff)))
        })


# ===============================
# DATAFRAME
# ===============================
df = pd.DataFrame(results)
df["speedup"] = df["scipy_time_ns"] / df["custom_time_ns"]


# ===============================
# PLOTTING
# ===============================
def plot_error_vs_time(df, pname):
    subset = df[df["problem"] == pname]
    safe = subset["safe_name"].iloc[0]

    plt.figure()
    plt.loglog(subset["custom_time_ns"], subset["l2_error"], "o-", label="Custom")
    plt.loglog(subset["scipy_time_ns"], subset["l2_error"], "s--", label="SciPy")

    plt.title(f"{pname}: Error vs Time")
    plt.xlabel("Time (ns)")
    plt.ylabel("L2 Error")
    plt.legend()
    plt.grid(True)

    plt.savefig(f"./benchmarking/results/figures/{safe}_error_vs_time.png")
    plt.close()


def plot_steps_vs_error(df, pname):
    subset = df[df["problem"] == pname]
    safe = subset["safe_name"].iloc[0]

    plt.figure()
    plt.loglog(subset["custom_steps"], subset["l2_error"], "o-", label="Custom")
    plt.loglog(subset["scipy_steps"], subset["l2_error"], "s--", label="SciPy")

    plt.title(f"{pname}: Steps vs Error")
    plt.xlabel("Steps")
    plt.ylabel("L2 Error")
    plt.legend()
    plt.grid(True)

    plt.savefig(f"./benchmarking/results/figures/{safe}_steps_vs_error.png")
    plt.close()


def plot_speedup(df, pname):
    subset = df[df["problem"] == pname]
    safe = subset["safe_name"].iloc[0]

    plt.figure()
    plt.semilogx(subset["rtol"], subset["speedup"], "o-")

    plt.title(f"{pname}: Speedup")
    plt.xlabel("rtol")
    plt.ylabel("Speedup")
    plt.grid(True)

    plt.savefig(f"./benchmarking/results/figures/{safe}_speedup.png")
    plt.close()


def plot_trajectory(name, t, y_custom, y_scipy):
    safe = safe_name(name)

    plt.figure()
    for i in range(y_custom.shape[1]):
        plt.plot(t, y_custom[:, i], label=f"Custom x{i}")
        plt.plot(t, y_scipy[:, i], "--", label=f"SciPy x{i}")

    plt.title(name)
    plt.legend()
    plt.grid(True)

    plt.savefig(f"./benchmarking/results/figures/{safe}_trajectory.png")
    plt.close()


# ===============================
# GENERATE PLOTS
# ===============================
for pname in df["problem"].unique():
    plot_error_vs_time(df, pname)
    plot_steps_vs_error(df, pname)
    plot_speedup(df, pname)


# ===============================
# TRAJECTORY
# ===============================
for f_py, f_njit, y0_vec in zip(problems_py, problems_njit, Y0):

    pname = " ".join(f_py.__name__.split('_')[:-2])

    sol_custom = rk45(f_njit, y0_vec, t_span, t_eval=t_eval)
    sol_scipy = solve_ivp(f_py, t_span, y0_vec, t_eval=t_eval)

    plot_trajectory(pname, t_eval, sol_custom["y"], sol_scipy.y.T)


# ===============================
# REPORT
# ===============================
with open("./benchmarking/results/report.md", "w") as f:

    f.write("# Solver Benchmark Report\n\n")

    for pname in df["problem"].unique():
        subset = df[df["problem"] == pname]
        safe = subset["safe_name"].iloc[0]
        best = subset.loc[subset["l2_error"].idxmin()]

        f.write(f"## {pname}\n\n")
        f.write(f"- Best L2 error: {best['l2_error']:.2e}\n")
        f.write(f"- Speedup: {best['speedup']:.2f}x\n\n")

        f.write(f"![Error vs Time](figures/{safe}_error_vs_time.png)\n\n")
        f.write(f"![Steps vs Error](figures/{safe}_steps_vs_error.png)\n\n")
        f.write(f"![Speedup](figures/{safe}_speedup.png)\n\n")
        f.write(f"![Trajectory](figures/{safe}_trajectory.png)\n\n")