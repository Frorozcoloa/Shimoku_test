from typing import Optional, Union
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

datasets = Path(__file__).resolve().parent.parent / "datasets"

def read_dataset()->pd.DataFrame:
    """Reads the dataset from a given path.

    Returns:
        pandas.DataFrame: The dataset.
    """
    offer_path = datasets / "raw" / "offers.csv"
    offer = pd.read_csv(offer_path)
    return offer

def delete_uniques_columns(df:pd.DataFrame)->pd.DataFrame:
    """Deletes the columns with unique values.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset without the columns with unique values.
    """
    df = df.drop(columns=["Id", "First Name"], axis=1)
    return df

def convert_to_datetime(df:pd.DataFrame)->pd.DataFrame:
    """Converts the date columns to datetime type and creates a new column for the duration of the offer.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with converted date columns.
    """
    df['Close Date'] = pd.to_datetime(df['Close Date'])
    df['Open Date'] = pd.to_datetime(df['Open Date'])
    df["Duration"] = (df["Close Date"] - df["Open Date"]).dt.days
    return df

def pre_proccesing_discont(df:pd.DataFrame)->pd.DataFrame:
    """Preprocesses the discount column.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with preprocessed discount column.
    """
    df['has_Discount_Code'] = ~df['Discount Code'].isnull()
    df.drop(columns=['Discount Code'], inplace=True)
    return df

def create_columns_null_values(df:pd.DataFrame)->pd.DataFrame:
    """Creates new columns for the null values of the dataset.
    Args:
        df (pandas.DataFrame): The dataset.
    Output:
        pandas.DataFrame: The dataset with new columns for the null values.
    """
    columns_with_null_values = df.columns[df.isnull().any()].tolist()
    for column in columns_with_null_values:
        name_new_column = column + '_isnull'
        name_new_column = name_new_column.replace(' ', '_')
        df[column + '_isnull'] = df[column].isnull()
    return df

def save_values(df, path: Union[str, Path] = None ):
    """Saves the preprocessed dataset.

    Args:
        df (pandas.DataFrame): The dataset.
    """
    if path is None:
        path = datasets / "processed" / "offer.csv"
    df.to_csv(path, index=False)
    

def preprocessing(df:pd.DataFrame, path_output = Optional[Path])->pd.DataFrame:
    """Preprocesses the dataset.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The preprocessed dataset.
    """
    df = delete_uniques_columns(df)
    df = convert_to_datetime(df)
    df = pre_proccesing_discont(df)
    df = create_columns_null_values(df)
    save_values(df, path_output)
    return df

        
        