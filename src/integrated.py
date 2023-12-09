from typing import Optional, Union
from pathlib import Path
import pandas as pd
from .utils import create_report, changes_columns, create_columns_null_values
datasets = Path(__file__).resolve().parent.parent / "datasets"

def read_datasets_leads()->pd.DataFrame:
    """Reads the dataset from a given path.

    Returns:
        pandas.DataFrame: The dataset.
    """
    path = datasets / "raw" / "leads.csv"
    leads = pd.read_csv(path)
    leads = leads.dropna(subset=["Id"])
    return leads

def preprocesing_city(df)->pd.DataFrame:
    """Preprocesses the city column.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with preprocessed city column.
    """
    df["has_city"] = ~df["City"].isnull()
    df.drop(columns=["City"], inplace=True)
    return df

def preprocessing_acquisition_campaign(df):
    """Preprocesses the Acquisition campaign column.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with preprocessed Acquisition campaign column.
    """
    major_values = ["VirtualMeetups", "EducationExpo", "TradeShow"]
    df["acquisition_campaign"] = df["Acquisition Campaign"].apply(lambda x: x if x in major_values else "Other")
    df.drop(columns=["Acquisition Campaign"], inplace=True)
    return df

def preprocesing_use_case(df)->pd.DataFrame:
    """Preprocesses the Use case column.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with preprocessed Use case column.
    """
    major_values = ["Corporate Events"]
    df["use_case"] = df["Use Case"].apply(lambda x: x if x in major_values else "Other")
    df.drop(columns=["Use Case"], inplace=True)
    return df

def preprocessing_source(df:pd.DataFrame)->pd.DataFrame:
    """Preprocesses the Source column.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with preprocessed Source column.
    """
    df["source"] = df["Source"]
    df.drop(columns=["Source"], inplace=True)
    return df

def preprocessing_created_date(df:pd.DataFrame)->pd.DataFrame:
    """Preprocesses the Created date column.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with preprocessed Created date column.
    """
    df["created_date"] = pd.to_datetime(df["Created Date"])
    df.drop(columns=["Created Date"], inplace=True)
    return df

def run():
    """Preprocesses the dataset and saves it in the processed folder.
    """
    df = read_datasets_leads()
    df = df[["Id", "City", "Acquisition Campaign", "Use Case", "Source", "Created Date"]]
    df = preprocesing_city(df)
    df = preprocessing_acquisition_campaign(df)
    df = preprocesing_use_case(df)
    df = preprocessing_source(df)
    df = preprocessing_created_date(df)
    df = changes_columns(df)
    #df = create_columns_null_values(df)
    create_report(df, "leads")
    df.to_csv(datasets / "processed" / "leads.csv", index=False)
