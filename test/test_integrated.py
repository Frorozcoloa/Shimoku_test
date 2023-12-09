import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from src.integrated import (
    read_datasets_leads,
    preprocesing_city,
    preprocessing_acquisition_campaign,
    preprocesing_use_case,
    preprocessing_source,
    preprocessing_created_date,
)

# Directorio de prueba
test_datasets = Path("test_datasets")

def test_read_datasets_leads():
    # Llamar a la función read_datasets_leads
    leads_df = read_datasets_leads()

    # Verificar que el resultado es un DataFrame y no es nulo
    assert isinstance(leads_df, pd.DataFrame)
    assert not leads_df.empty

    # Verificar que no hay valores nulos en la columna 'Id'
    assert not leads_df['Id'].isnull().any()

def test_preprocesing_city():
    # Crear un DataFrame de prueba con la columna 'City'
    df = pd.DataFrame({
        'City': ['New York', 'Chicago', np.nan]
    })

    # Llamar a la función preprocesing_city
    result_df = preprocesing_city(df)

    # Verificar que el resultado es un DataFrame y no es nulo
    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty

    # Verificar que la columna 'has_city' se ha creado correctamente
    assert 'has_city' in result_df.columns

def test_preprocessing_acquisition_campaign():
    # Crear un DataFrame de prueba con la columna 'Acquisition campaign'
    df = pd.DataFrame({
        'Acquisition Campaign': ['VirtualMeetups', 'EducationExpo', 'Other']
    })

    # Llamar a la función preprocessing_acquisition_campaign
    result_df = preprocessing_acquisition_campaign(df)

    # Verificar que el resultado es un DataFrame y no es nulo
    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty

    # Verificar que la columna 'acquisition_campaign' se ha creado correctamente
    assert 'acquisition_campaign' in result_df.columns

def test_preprocesing_use_case():
    # Crear un DataFrame de prueba con la columna 'Use case'
    df = pd.DataFrame({
        'Use Case': ['Corporate ', 'eventes', 'Other']
    })

    # Llamar a la función preprocesing_use_case
    result_df = preprocesing_use_case(df)

    # Verificar que el resultado es un DataFrame y no es nulo
    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty

    # Verificar que la columna 'use_case' se ha creado correctamente
    assert 'use_case' in result_df.columns

def test_preprocessing_source():
    # Crear un DataFrame de prueba con la columna 'Source'
    df = pd.DataFrame({
        'Source': ['Google', 'Facebook', 'Other']
    })

    # Llamar a la función preprocessing_source
    result_df = preprocessing_source(df)

    # Verificar que el resultado es un DataFrame y no es nulo
    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty

    # Verificar que la columna 'source' se ha creado correctamente
    assert 'source' in result_df.columns

def test_preprocessing_created_date():
    # Crear un DataFrame de prueba con la columna 'Created date'
    df = pd.DataFrame({
        'Created Date': ['2022-01-01', '2022-02-01']
    })

    # Llamar a la función preprocessing_created_date
    result_df = preprocessing_created_date(df)

    # Verificar que el resultado es un DataFrame y no es nulo
    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty

    # Verificar que la columna 'created_date' se ha creado correctamente
    assert 'created_date' in result_df.columns
