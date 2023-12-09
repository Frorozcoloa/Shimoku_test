from typing import Optional, Union
from pathlib import Path
import pandas as pd

from .utils import create_report, changes_columns, create_columns_null_values

datasets = Path(__file__).resolve().parent.parent / "datasets"

def create_binary_columns(df:pd.DataFrame)->pd.DataFrame:
    """Creates binary columns for the categorical columns.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with binary columns.
    """
    filtered_df = df[df['Status'].isin(['Closed Won', 'Closed Lost'])]
    return filtered_df

def read_dataset()->pd.DataFrame:
    """Reads the dataset from a given path.

    Returns:
        pandas.DataFrame: The dataset.
    """
    offer_path = datasets / "raw" / "offers.csv"
    offer = pd.read_csv(offer_path)
    return offer


def convert_to_datetime(df:pd.DataFrame)->pd.DataFrame:
    """Converts the date columns to datetime type and creates a new column for the duration of the offer.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with converted date columns.
    """
    df['Close Date'] = pd.to_datetime(df['Close Date'])
    df['Created Date'] = pd.to_datetime(df['Created Date'])
    df["Duration"] = (df["Close Date"] - df["Created Date"]).dt.days
    return df

def pre_proccesing_discont(df:pd.DataFrame)->pd.DataFrame:
    """Preprocesses the discount column.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with preprocessed discount column.
    """
    df['has_Discount_Code'] = ~df['Discount code'].isnull()
    df.drop(columns=['Discount code'], inplace=True)
    return df

def pre_proccesing_use_case(df:pd.DataFrame)->pd.DataFrame:
    """Preprocesses the use case column.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with preprocessed use case column.
    """
    major_class = ["Corporate Events"]
    df["was_corporate_event"] = df["Use Case"].isin(major_class)
    df.drop(columns=["Use Case"], inplace=True)
    return df

def preprocessing_pain(df:pd.DataFrame)->pd.DataFrame:
    """Preprocesses the pain column.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with preprocessed pain column.
    """
    major = ["operations"]
    df["pain"] = df["Pain"].isin(major)
    df.drop(columns=["Pain"], inplace=True)
    return df


def save_values(df, path: Union[str, Path] = None ):
    """Saves the preprocessed dataset.

    Args:
        df (pandas.DataFrame): The dataset.
    """
    if path is None:
        path = datasets / "processed" / "offer.csv"
    df.to_csv(path, index=False)


def preprocessing(df:pd.DataFrame, path_output: Optional[Path] = None)->pd.DataFrame:
    """Preprocesses the dataset.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The preprocessed dataset.
    """
    df = create_binary_columns(df)
    df = convert_to_datetime(df)
    df = pre_proccesing_discont(df)
    df = pre_proccesing_use_case(df)
    df = preprocessing_pain(df)
    df = changes_columns(df)
    save_values(df, path_output)
    create_report(df, "offer")
    return df

        
def run():
    df = read_dataset()
    preprocessing(df)