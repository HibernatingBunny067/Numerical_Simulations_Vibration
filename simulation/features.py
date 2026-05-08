import numpy as np
from numpy.typing import NDArray
from typing import Dict


def entropy(psd_norm: NDArray) -> float:
    return (-np.sum(psd_norm * np.log2(psd_norm))).item()


def dominant_frequency(signal: NDArray, dt: float) -> tuple[float, float]:
    """
    Returns:
    --------
    dominant_freq : float
    dominant_amp  : float
    """

    signal = signal - np.mean(signal)

    fft_complex = np.fft.rfft(signal)

    psd = np.abs(fft_complex) ** 2

    freqs = np.fft.rfftfreq(len(signal), d=dt)

    peak_idx = np.argmax(psd[1:]) + 1

    dominant_freq = freqs[peak_idx]
    dominant_amp = psd[peak_idx]

    return dominant_freq.item(), dominant_amp.item()


def extract_features(
    result: Dict,
    get_transients: bool = False
) -> Dict[str, float]:

    X = result['y'][:, 0]
    Y = result['y'][:, 1]
    Xdot = result['y'][:, 2]
    Ydot = result['y'][:, 3]
    t = result['t']

    R = np.sqrt(X**2 + Y**2)

    # ----------------------------
    # steady-state window
    # ----------------------------

    if not get_transients:

        ss = slice(int(0.7 * len(R)), None)

        X = X[ss]
        Y = Y[ss]

        Xdot = Xdot[ss]
        Ydot = Ydot[ss]

        R = R[ss]
        t = t[ss]

    # ----------------------------
    # contact metrics
    # ----------------------------

    penetration = np.maximum(R - 1.0, 0.0)

    # ----------------------------
    # spectral analysis
    # ----------------------------

    dt = np.mean(np.diff(t))

    # x-spectrum
    x_dom_freq, x_dom_amp = dominant_frequency(X, dt)

    # y-spectrum
    y_dom_freq, y_dom_amp = dominant_frequency(Y, dt)

    # effective whirl frequency
    whirl_freq = 0.5 * (x_dom_freq + y_dom_freq)

    # radial complexity spectrum
    radial_signal = R - np.mean(R)

    radial_fft = np.fft.rfft(radial_signal)

    radial_psd = np.abs(radial_fft) ** 2

    radial_psd += 1e-12

    psd_norm = radial_psd / np.sum(radial_psd)

    psd_norm = np.clip(psd_norm, 1e-12, None)

    spectral_entropy = entropy(psd_norm)

    # crest factor
    radial_rms = np.sqrt(np.mean(radial_signal**2))

    crest_factor = (
        np.max(np.abs(radial_signal)) / (radial_rms + 1e-12)
    ).item()

    # ----------------------------
    # final features
    # ----------------------------

    return {

        # orbit statistics
        "R_mean": np.mean(R).item(),
        "R_std": np.std(R).item(),
        "R_max": np.max(R).item(),
        "R_min": np.min(R).item(),

        # contact mechanics
        "contact_ratio": np.mean(R > 1.0).item(),
        "penetration_mean": np.mean(penetration).item(),
        "penetration_max": np.max(penetration).item(),

        # dynamics
        "velocity_rms":
            np.sqrt(np.mean(Xdot**2 + Ydot**2)).item(),

        # orbit spread
        "x_std": np.std(X).item(),
        "y_std": np.std(Y).item(),

        "orbit_dispersion":
            (np.pi * np.std(X) * np.std(Y)).item(),

        # spectral features
        "x_dom_freq": x_dom_freq,
        "x_dom_amp": x_dom_amp,

        "y_dom_freq": y_dom_freq,
        "y_dom_amp": y_dom_amp,

        "whirl_freq": whirl_freq,

        "spectral_entropy": spectral_entropy,

        "crest_factor": crest_factor
    }