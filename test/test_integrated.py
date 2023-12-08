import pandas as pd
from pathlib import Path
import pytest
from src.integrated import read_lead, get_ids, save_values, preprocessing, changes_columns

# Directorio de prueba
datasets = Path(__file__).resolve().parent.parent / "datasets"

def test_read_lead():
    # Llamar a la función read_lead
    lead_df = read_lead()

    # Verificar que el resultado es un DataFrame y no es nulo
    assert isinstance(lead_df, pd.DataFrame)
    assert not lead_df.empty

def test_get_ids():
    # Crear un DataFrame de prueba con la columna 'Id'
    df = pd.DataFrame({
        'Id': [1, 2, 3, 1, 2, 3, 4, 5, 6]
    })

    # Llamar a la función get_ids
    result_df = get_ids(df)

    # Verificar que el resultado es un DataFrame y no es nulo
    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty

    # Verificar que solo contiene valores únicos de 'Id'
    assert result_df['Id'].nunique() == len(result_df)

def test_save_values(tmp_path):
    # Crear un DataFrame de prueba con la columna 'Id'
    df = pd.DataFrame({
        'Id': [1, 2, 3]
    })

    # Llamar a la función save_values
    save_values(df, path=tmp_path / "ids.csv")

    # Verificar que el archivo CSV fue creado en la ubicación esperada
    expected_file_path = tmp_path / "ids.csv"
    assert expected_file_path.is_file()

    # Limpiar el archivo creado durante la prueba
    expected_file_path.unlink()

def test_preprocessing(tmp_path):
    # Crear un DataFrame de prueba con la columna 'Id'
    df = pd.DataFrame({
        'Id': [1, 2, 3, 1, 2, 3, 4, 5, 6]
    })

    # Llamar a la función preprocessing
    result_df = preprocessing(df, path_output=tmp_path / "ids.csv")

    # Verificar que el resultado es un DataFrame y no es nulo
    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty

    # Verificar que solo contiene valores únicos de 'Id'
    assert result_df['Id'].nunique() == len(result_df)

    # Verificar que el archivo CSV fue creado en la ubicación esperada
    expected_file_path = tmp_path / "ids.csv"
    assert expected_file_path.is_file()

    # Limpiar el archivo creado durante la prueba
    expected_file_path.unlink()
    

def test_changes_columns():
    # Crear un DataFrame de prueba con nombres de columnas específicos
    df = pd.DataFrame({
        'First Name': ['John', 'Jane'],
        'Last Name': ['Doe', 'Smith'],
        'Age': [25, 30]
    })

    # Llamar a la función changes_columns
    result_df = changes_columns(df)

    # Verificar que el resultado es un DataFrame y no es nulo
    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty

    # Verificar que los nombres de las columnas se han cambiado correctamente
    expected_columns = ['first_name', 'last_name', 'age']
    assert result_df.columns.tolist() == expected_columns

    # Verificar que los datos del DataFrame se mantienen intactos
    assert result_df['first_name'].tolist() == ['John', 'Jane']
    assert result_df['last_name'].tolist() == ['Doe', 'Smith']
    assert result_df['age'].tolist() == [25, 30]
