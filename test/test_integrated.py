import sys
sys.path.append("..")
import pandas as pd
import pytest
from src.integrated import read_datasets_leads, preprocesing_city, preprocessing_acquisition_campaign, preprocessing_source, preprocessing_created_date

@pytest.fixture
def sample_leads_df():
    # Create a sample leads DataFrame for testing
    return pd.DataFrame({
        'Id': [1, 2, 3],
        'City': ['City1', 'City2', None],
        'Acquisition Campaign': ['Campaign1', None, 'Campaign3'],
        'Source': ['Source1', 'Source2', 'Source3'],
        'Created Date': ['2022-01-01', '2022-02-02', '2022-03-03']
    })

def test_read_datasets_leads(sample_leads_df):
    df_leads = read_datasets_leads()
    assert isinstance(df_leads, pd.DataFrame)
    assert not df_leads.empty

def test_preprocesing_city(sample_leads_df):
    df_preprocessed = preprocesing_city(sample_leads_df)
    assert isinstance(df_preprocessed, pd.DataFrame)
    assert 'has_city' in df_preprocessed.columns
    assert all(isinstance(value, bool) for value in df_preprocessed['has_city'])

def test_preprocessing_acquisition_campaign(sample_leads_df):
    df_preprocessed = preprocessing_acquisition_campaign(sample_leads_df)
    assert isinstance(df_preprocessed, pd.DataFrame)
    assert 'has_acquisition_campaign' in df_preprocessed.columns
    assert all(isinstance(value, bool) for value in df_preprocessed['has_acquisition_campaign'])



def test_preprocessing_created_date(sample_leads_df):
    df_preprocessed = preprocessing_created_date(sample_leads_df)
    assert isinstance(df_preprocessed, pd.DataFrame)
    assert 'created_date' in df_preprocessed.columns
    assert pd.api.types.is_datetime64_ns_dtype(df_preprocessed['created_date'])

# Add more tests as needed
