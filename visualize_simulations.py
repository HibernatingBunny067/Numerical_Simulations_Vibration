import json
import numpy as np
import matplotlib.pyplot as plt

def load_n_results(filename, n=2):
    results = []

    with open(filename, 'r') as f:
        for line in f:
            entry = json.loads(line)
            if entry["status"] == "ok":
                results.append(entry)
                if len(results) >= n:
                    break

    return results

def visualize_results(results):
    n = len(results)
    fig, axes = plt.subplots(n, 3, figsize=(16, 4*n))

    if n == 1:
        axes = [axes]

    for i, entry in enumerate(results):
        ts = np.array(entry["ts"])
        ys = np.array(entry["ys"])
        key = entry["key"]
        params = np.array(entry["params_array"])

        omega_n = params[0]
        zeta = params[1]

        x = ys[:, 0]
        v = ys[:, 1]

        peak_amp = np.max(np.abs(x))

        fft = np.fft.rfft(x)
        freqs = np.fft.rfftfreq(len(ts), d=ts[1]-ts[0])
        dominant_freq = freqs[np.argmax(np.abs(fft))]

        info = (
            f"ωₙ={omega_n:.2f}, ζ={zeta:.2f}\n"
            f"f_shaft={key['f_shaft']:.2f}, sev={key['severity']:.2f}\n"
            f"peak={peak_amp:.2f}, f_dom={dominant_freq:.2f}"
        )

        axes[i][0].plot(ts, x)
        axes[i][0].set_title("x(t)")
        axes[i][0].text(0.02, 0.95, info, transform=axes[i][0].transAxes,
                        verticalalignment='top', fontsize=9,
                        bbox=dict(boxstyle="round", alpha=0.2))

        axes[i][1].plot(x, v)
        axes[i][1].set_title("Phase Space")

        axes[i][2].plot(freqs, np.abs(fft))
        axes[i][2].set_title("FFT")

    plt.tight_layout()
    plt.show()

def main():
    results = load_n_results("simulation_results.jsonl", n=2)
    visualize_results(results)

if __name__ == "__main__":
    main()