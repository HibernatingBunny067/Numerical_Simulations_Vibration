import os
import pandas as pd
import numpy as np
from numpy.typing import NDArray
from typing import Dict,Optional

RESULTS_DIR = r'results'
RAW_DIR = os.path.join(RESULTS_DIR,"raw")
META_DIR = os.path.join(RESULTS_DIR,"metadata")

def save_result(params:Dict,
                trajectory:Optional[Dict]=None,
                save_raw:bool=False,
                filename:Optional[str]=None,
                metafile_name:Optional[str] = "metadata.csv") -> None:
    
    os.makedirs(RAW_DIR,exist_ok=True)
    os.makedirs(META_DIR,exist_ok=True)
    
    if trajectory is not None and save_raw:

        filename = (
            f"{filename}.npz" 
            if filename is not None 
            else f"{np.random.randint(0,100000)}.npz"
        )
        store_path = os.path.join(RAW_DIR,filename)

        np.savez_compressed(
            store_path,
            t =trajectory['t'],
            y = trajectory['y']
        )

    metadata_path = os.path.join(META_DIR,metafile_name)

    df = pd.DataFrame([params])

    write_header = not os.path.exists(metadata_path)

    df.to_csv(
        metadata_path,
        mode='a',
        header=write_header,
        index=True
    )