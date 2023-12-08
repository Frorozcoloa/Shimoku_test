from typing import Optional, Union, List
from pathlib import Path
import pandas as pd

datasets = Path(__file__).resolve().parent.parent / "datasets"

def read_dataset_offer()->List[pd.DataFrame]:
    """Reads the dataset from a given path.

    Returns:
        pandas.DataFrame: The dataset.
    """
    offer_path = datasets / "process" / "offers.csv"
    lead_path = datasets / "process" / "leads.csv"
    offer = pd.read_csv(offer_path)
    lead = pd.read_csv(lead_path)
    return [offer, lead]

def join_datasets(df:List[pd.DataFrame])->pd.DataFrame:
    """Joins the datasets.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with the ids.
    """
    pass