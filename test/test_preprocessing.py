from pathlib import Path
import pandas as pd
import numpy as np
from src.preprocessing import (
    read_dataset,
    delete_uniques_columns,
    convert_to_datetime,
    pre_proccesing_discont,
    create_columns_null_values,
    preprocessing,
    save_values
)
TEST_DATASETS = Path(__file__).resolve().parent / "datasets"

def test_read_dataset():
    # Puedes cambiar la ruta del archivo según tu configuración
    df = read_dataset()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_delete_uniques_columns():
    # Crear un DataFrame de prueba
    df = pd.DataFrame({
        'Id': [1, 2, 3],
        'First Name': ['John', 'Jane', 'Bob'],
        'Other Column': ['A', 'B', 'C']
    })

    result_df = delete_uniques_columns(df)
    # Asegurar que las columnas 'Id' y 'First Name' se han eliminado
    assert 'Id' not in result_df.columns
    assert 'First Name' not in result_df.columns
    # Asegurar que otras columnas se mantienen
    assert 'Other Column' in result_df.columns

def test_convert_to_datetime():
    # Crear un DataFrame de prueba con columnas de fecha
    df = pd.DataFrame({
        'Open Date': ['2022-01-01', '2022-02-01'],
        'Close Date': ['2022-01-10', '2022-02-10'],
    })

    result_df = convert_to_datetime(df)
    # Asegurar que las columnas 'Open Date' y 'Close Date' son de tipo datetime
    assert pd.api.types.is_datetime64_any_dtype(result_df['Open Date'])
    assert pd.api.types.is_datetime64_any_dtype(result_df['Close Date'])
    # Asegurar que la columna 'Duration' se ha creado correctamente
    assert 'Duration' in result_df.columns

def test_pre_proccesing_discont():
    # Crear un DataFrame de prueba con la columna 'Discount Code'
    df = pd.DataFrame({
        'Discount Code': ['A', np.nan, 'B']
    })

    result_df = pre_proccesing_discont(df)
    # Asegurar que la columna 'Discount Code' se ha eliminado
    assert 'Discount Code' not in result_df.columns
    # Asegurar que la columna 'has_Discount_Code' se ha creado correctamente
    assert 'has_Discount_Code' in result_df.columns

def test_create_columns_null_values():
    # Crear un DataFrame de prueba con valores nulos
    df = pd.DataFrame({
        'Column1': [1, 2, np.nan],
        'Column2': ['A', np.nan, 'C']
    })

    result_df = create_columns_null_values(df)
    # Asegurar que se han creado nuevas columnas para los valores nulos
    assert 'Column1_isnull' in result_df.columns
    assert 'Column2_isnull' in result_df.columns

def test_save_values():
    # Crear un DataFrame de prueba
    df = pd.DataFrame({
        'Column1': [1, 2, 3],
        'Column2': ['A', 'B', 'C']
    })

    # Llamar a la función save_values
    path = TEST_DATASETS / "offer.csv"
    save_values(df, path=path)

    # Verificar si el archivo CSV fue creado en la ubicación esperada
    expected_file_path = TEST_DATASETS / "offer.csv"
    assert expected_file_path.is_file()

    # Limpiar el archivo creado durante la prueba
    expected_file_path.unlink()

def test_preprocessing():
    # Crear un DataFrame de prueba
    df = pd.DataFrame({
        'Id': [1, 2, 3],
        'First Name': ['John', 'Jane', 'Bob'],
        'Open Date': ['2022-01-01', '2022-02-01', '2022-03-01'],
        'Close Date': ['2022-01-10', '2022-02-10', '2022-03-10'],
        'Discount Code': ['A', 'B', np.nan]
    })
    path_test = TEST_DATASETS / "offer.csv"
    # Llamar a la función preprocessing
    result_df = preprocessing(df, path_output=path_test)

    # Verificar que el resultado es un DataFrame y no es nulo
    assert isinstance(result_df, pd.DataFrame)
    assert not result_df.empty

    # Verificar que las columnas esperadas se han creado o eliminado durante el preprocesamiento
    assert 'Id' not in result_df.columns
    assert 'First Name' not in result_df.columns
    assert pd.api.types.is_datetime64_any_dtype(result_df['Open Date'])
    assert pd.api.types.is_datetime64_any_dtype(result_df['Close Date'])
    assert 'Duration' in result_df.columns
    assert 'Discount Code' not in result_df.columns
    assert 'has_Discount_Code' in result_df.columns

    # Limpiar el archivo creado durante la prueba
    file_path = TEST_DATASETS /  "offer.csv"
    file_path.unlink()