import numpy as np
from numpy.typing import NDArray
from typing import Dict

def extract_features(result:Dict) -> Dict[str,float]:
    X = result['y'][:,0]
    Y = result['y'][:,1]

    R = np.sqrt(X**2 + Y**2)

    # ss = slice(len(R)//2,None)

    R_ss = R

    return {
        "R_mean": np.mean(R_ss).item(),
        "R_std": np.std(R_ss).item(),
        "contact_ratio": np.mean(R_ss > 1.0).item()
    }