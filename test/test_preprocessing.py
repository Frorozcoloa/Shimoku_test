import sys
sys.path.append("..")

import pandas as pd
import pytest
from src.preprocessing import create_binary_columns, read_dataset, convert_to_datetime, pre_proccesing_discont, pre_proccesing_use_case, preprocessing_pain, changes_columns, save_values, preprocessing

@pytest.fixture
def sample_offer_df():
    # Create a sample offer DataFrame for testing
    return pd.DataFrame({
        'Status': ['Closed Won', 'Closed Lost', 'Open'],
        'Close Date': ['2022-01-01', '2022-02-02', '2022-03-03'],
        'Created Date': ['2022-01-01', '2022-02-02', '2022-03-03'],
        'Discount code': ['ABC123', None, 'XYZ789'],
        'Use Case': ['Corporate Events', 'Other', 'Corporate Events'],
        'Pain': ['operations', 'sales', 'marketing']
    })

def test_create_binary_columns(sample_offer_df):
    df_binary = create_binary_columns(sample_offer_df)
    assert isinstance(df_binary, pd.DataFrame)
    assert 'Status' in df_binary.columns
    assert all(value in ['Closed Won', 'Closed Lost'] for value in df_binary['Status'])


def test_convert_to_datetime(sample_offer_df):
    df_datetime = convert_to_datetime(sample_offer_df)
    assert isinstance(df_datetime, pd.DataFrame)
    assert 'Close Date' in df_datetime.columns
    assert 'Created Date' in df_datetime.columns
    assert 'Duration' in df_datetime.columns
    assert pd.api.types.is_datetime64_ns_dtype(df_datetime['Close Date'])
    assert pd.api.types.is_datetime64_ns_dtype(df_datetime['Created Date'])
    assert pd.api.types.is_int64_dtype(df_datetime['Duration'])

def test_pre_proccesing_discont(sample_offer_df):
    df_preprocessed = pre_proccesing_discont(sample_offer_df)
    assert isinstance(df_preprocessed, pd.DataFrame)
    assert 'has_Discount_Code' in df_preprocessed.columns
    assert all(isinstance(value, bool) for value in df_preprocessed['has_Discount_Code'])

def test_pre_proccesing_use_case(sample_offer_df):
    df_preprocessed = pre_proccesing_use_case(sample_offer_df)
    assert isinstance(df_preprocessed, pd.DataFrame)
    assert 'was_corporate_event' in df_preprocessed.columns
    assert all(isinstance(value, bool) for value in df_preprocessed['was_corporate_event'])

def test_preprocessing_pain(sample_offer_df):
    df_preprocessed = preprocessing_pain(sample_offer_df)
    assert isinstance(df_preprocessed, pd.DataFrame)
    assert 'pain' in df_preprocessed.columns
    assert all(isinstance(value, bool) for value in df_preprocessed['pain'])

def test_save_values(sample_offer_df, tmp_path):
    # Using a temporary directory for testing file saving
    output_path = tmp_path / 'test_offer.csv'
    save_values(sample_offer_df, output_path)
    assert output_path.exists()