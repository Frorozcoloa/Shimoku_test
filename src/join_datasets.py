from typing import Optional, Union, List
from pathlib import Path
import pandas as pd
import numpy as np
from .utils import create_report, create_columns_null_values

datasets = Path(__file__).resolve().parent.parent / "datasets"

def read_dataset_offer()->List[pd.DataFrame]:
    """Reads the dataset from a given path.

    Returns:
        pandas.DataFrame: The dataset.
    """
    offer_path = datasets / "processed" / "offer.csv"
    offer = pd.read_csv(offer_path)
    return offer
    

def read_dataset_leads():
    """Joins the datasets.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with the ids.
    """
    path = datasets / "processed" / "leads.csv"
    leads = pd.read_csv(path)
    return leads

def merge_datasets(df_lead:pd.DataFrame, df_offer:pd.DataFrame)->pd.DataFrame:
    """Merges the datasets.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with the ids.
    """
    df_lead = df_lead.add_prefix('lead_')
    df = pd.merge(df_offer, df_lead, left_on="id", right_on="lead_id", how="left")
    df_lead = df_lead.drop(columns=['lead_id', 'lead_created_date'])
    df["duration_created"] = (pd.to_datetime(df["created_date"]) - pd.to_datetime(df["lead_created_date"]))/np.timedelta64(1, 'D')
    df = df.drop(columns=['lead_id', 'id', 'lead_created_date', 'created_date'])
    #colums_lead = ["lead_has_city", "lead_acquisition_campaign", "lead_use_case", "lead_source"]
    return df

def  preprocessing_close_date(df:pd.DataFrame)->pd.DataFrame:
    df = df.drop(columns=["close_date"])
    df = df.drop(columns=["loss_reason", "loss_reason_isnull"])
    return df

def run():
    df_offer = read_dataset_offer()
    df_lead = read_dataset_leads()
    df = merge_datasets(df_lead, df_offer)
    df = create_columns_null_values(df)
    df = preprocessing_close_date(df)
    create_report(df, 'integrated')
    df.to_csv(datasets / "processed" / "integrated.csv", index=False)
    return df