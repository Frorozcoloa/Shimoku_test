import sys
sys.path.append("..")
from src.preprocessing import (
    read_dataset,
    delete_uniques_columns,
    convert_to_datetime,
    pre_proccesing_discont,
    create_columns_null_values,
    preprocessing,
    save_values
)
import pandas as pd
import pytest
from your_module import read_datasets_leads, preprocesing_city, preprocessing_acquisition_campaign, preprocessing_source, preprocessing_created_date, run

@pytest.fixture
def sample_leads_df():
    # Puedes crear un DataFrame de ejemplo para tus pruebas
    return pd.DataFrame({
        'Id': [1, 2, 3],
        'City': ['City1', 'City2', None],
        'Acquisition Campaign': ['Campaign1', None, 'Campaign3'],
        'Source': ['Source1', 'Source2', 'Source3'],
        'Created Date': ['2022-01-01', '2022-02-02', '2022-03-03']
    })

def test_read_datasets_leads(sample_leads_df):
    df = read_datasets_leads()
    assert isinstance(df, pd.DataFrame)
    assert not df["Id"].isnull().any()  # Asegurar que no hay valores nulos en la columna "Id"

def test_preprocesing_city(sample_leads_df):
    df = preprocesing_city(sample_leads_df)
    assert "has_city" in df.columns
    assert all(isinstance(value, bool) for value in df["has_city"])

def test_preprocessing_acquisition_campaign(sample_leads_df):
    df = preprocessing_acquisition_campaign(sample_leads_df)
    assert "has_acquisition_campaign" in df.columns
    assert all(isinstance(value, bool) for value in df["has_acquisition_campaign"])

def test_preprocessing_source(sample_leads_df):
    df = preprocessing_source(sample_leads_df)
    assert "source" in df.columns
    assert all(value in df["source"].unique() for value in sample_leads_df["Source"])

def test_preprocessing_created_date(sample_leads_df):
    df = preprocessing_created_date(sample_leads_df)
    assert "created_date" in df.columns
    assert pd.api.types.is_datetime64_ns_dtype(df["created_date"])


