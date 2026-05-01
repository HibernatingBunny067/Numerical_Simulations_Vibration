from scipy.interpolate import CubicHermiteSpline
from numpy.typing import NDArray

def interpolated_results(t_uniform:NDArray,ts:NDArray,ys:NDArray,fs:NDArray) -> NDArray:
    spline = CubicHermiteSpline(
        ts,
        ys,
        fs
    )
    return spline(t_uniform)