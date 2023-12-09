import pandas as pd
import pytest
from src.join_datasets import read_dataset_offer, read_dataset_leads, merge_datasets, preprocessing_close_date, run

@pytest.fixture
def sample_df_offer():
    # You may want to create some sample data for testing
    return pd.DataFrame({'id': [1, 2], 'col1': ['A', 'B']})

@pytest.fixture
def sample_df_leads():
    # You may want to create some sample data for testing
    return pd.DataFrame({'lead_id': [1, 2], 'lead_col1': ['X', 'Y']})

def test_read_dataset_offer():
    df_offer = read_dataset_offer()
    assert isinstance(df_offer, pd.DataFrame)
    assert len(df_offer) > 0  # Check if the DataFrame is not empty

def test_read_dataset_leads():
    df_leads = read_dataset_leads()
    assert isinstance(df_leads, pd.DataFrame)
    assert len(df_leads) > 0  # Check if the DataFrame is not empty

def test_merge_datasets(sample_df_leads, sample_df_offer):
    merged_df = merge_datasets(sample_df_leads, sample_df_offer)
    assert isinstance(merged_df, pd.DataFrame)
    assert len(merged_df) > 0  # Check if the DataFrame is not empty

def test_preprocessing_close_date():
    df_input = pd.DataFrame({'col1': [1, 2], 'close_date': ['2022-01-01', '2022-02-01']})
    processed_df = preprocessing_close_date(df_input)
    assert isinstance(processed_df, pd.DataFrame)
    assert 'close_date' not in processed_df.columns  # Check if the 'close_date' column is removed

def test_run():
    result_df = run()
    assert isinstance(result_df, pd.DataFrame)
    assert len(result_df) > 0  # Check if the DataFrame is not empty
