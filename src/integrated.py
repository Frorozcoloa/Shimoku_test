from typing import Optional, Union
from pathlib import Path
import pandas as pd

datasets = Path(__file__).resolve().parent.parent / "datasets"

def read_lead():
    """Reads the dataset from a given path.

    Returns:
        pandas.DataFrame: The dataset.
    """
    lead_path = datasets / "raw" / "leads.csv"
    lead = pd.read_csv(lead_path)
    return lead

def get_ids(df:pd.DataFrame)->pd.DataFrame:
    """Gets the ids of the dataset.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with the ids.
    """
    serie_id = df["Id"].dropna()
    uniques_id = serie_id.unique()
    df_id = pd.DataFrame(uniques_id, columns=["Id"])
    return df_id

def save_values(df:pd.DataFrame, path: Optional[Path] = None)->pd.DataFrame:
    """Saves the ids of the dataset.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with the ids.
    """
    if path is None:
        path = datasets / "processed" / "ids.csv"
    df.to_csv(path, index=False)
    
def preprocessing(df:pd.DataFrame, path_output: Optional[Path] = None)->pd.DataFrame:
    """Preprocesses the dataset.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The preprocessed dataset.
    """
    df = get_ids(df)
    save_values(df, path_output)
    return df

if __name__ == "__main__":
    df = read_lead()
    preprocessing(df)