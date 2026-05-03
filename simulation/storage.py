import os
import pandas as pd
import numpy as np
from numpy.typing import NDArray
from typing import Dict


RESULTS_DIR = r'results/raw'
META_FILE = r'results/metadata.csv'


def save_result(result:Dict[str,NDArray],params:Dict,save_raw:bool = False) -> None:

    os.makedirs(RESULTS_DIR,exist_ok=True)

    file_id = np.random.randint(0,1000000000)
    filename:str = f"{RESULTS_DIR}/{file_id}.npz"

    if save_raw:
        np.savez(filename,**result)

    row = {**params,"file":filename}

    if os.path.exists(META_FILE):
        df = pd.read_csv(META_FILE)
        df = pd.concat((df,pd.DataFrame([row])),ignore_index=True)
    else:
        df= pd.DataFrame([row])

    df.to_csv(META_FILE,index=False)