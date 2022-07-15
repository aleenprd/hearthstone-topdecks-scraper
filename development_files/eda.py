# %%
import pandas as pd
import os 
from typing import Dict, List, dict

path = "../data"


# %%
def read_datasets(path: str, verbose: bool=False) -> Dict[str, pd.DataFrame]:
    """Read all csv files at specified path, store in dictionary with 
    file names as keys and dataframes as values.
    
    Args:
        path (str): base directory path from where to fetch data.
        
    Returns:
        datasets (Dict[pd.Dataframe]): datasets collection. 
    """
    file_paths = [f"{path}/{x}" for x in os.listdir(path) if ".csv" in x]

    datasets = {}
    for file in file_paths:
        key = file.split(".")[-2].split("/")[-1]
        try:
            datasets[key] = pd.read_csv(file, encoding="utf-8")
        except:
            datasets[key] = pd.read_csv(file, encoding="ISO-8859-1")
    
    if verbose:
        print("Datasets:\n", list(datasets.keys()))
    
    return datasets

# %%
datasets = read_datasets(path, True)
# %%
hstd_all_urls = datasets["hstd_all_urls"]
hstd_all_cards_merged = datasets["hstd_all_cards_merged"]
hstd_all_cards = datasets["hstd_all_cards"]
hstd_failed_cards = datasets["hstd_failed_cards"]
# %%
hstd_all_cards_merged.columns
# %%
hstd_all_urls.columns
# %%
