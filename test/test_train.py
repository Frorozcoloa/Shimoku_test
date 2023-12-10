import pandas as pd
import pytest
import sys
sys.path.append("..")
from src.train import read_dataset, crate_colums, convert_to_categorical, split_datasets, train_model, tuned_model, evaluted_model, upload_graphics, calculated_auc, test_evaluated, get_score, run

@pytest.fixture
def sample_df():
    # You may want to create some sample data for testing
    return pd.DataFrame({'col1': [1, 2], 'col2': ['A', 'B'], 'status': [0, 1]})

def test_read_dataset(sample_df):
    with pytest.raises(FileNotFoundError):
        # Assuming the file does not exist for the test
        read_dataset()

def test_crate_colums(sample_df):
    bool_cols, numerical_cols, categorical_cols = crate_colums(sample_df)
    assert isinstance(bool_cols, list)
    assert isinstance(numerical_cols, list)
    assert isinstance(categorical_cols, list)

def test_convert_to_categorical(sample_df):
    df, values = convert_to_categorical(sample_df)
    assert isinstance(df, pd.DataFrame)
    assert isinstance(values, dict)

def test_split_datasets(sample_df):
    df_train, df_test = split_datasets(sample_df)
    assert isinstance(df_train, pd.DataFrame)
    assert isinstance(df_test, pd.DataFrame)

def test_train_model(sample_df):
    best_model = train_model(sample_df)
    assert isinstance(best_model, pd.DataFrame)

def test_tuned_model(sample_df):
    best_model = train_model(sample_df)
    tuned_model_result = tuned_model(best_model)
    assert isinstance(tuned_model_result, pd.DataFrame)

def test_evaluted_model(sample_df):
    evaluted_model_result = evaluted_model()
    assert evaluted_model_result is None  # Assuming it does not return anything

def test_upload_graphics(sample_df):
    best_model = train_model(sample_df)
    tuned_model_result = tuned_model(best_model)
    upload_graphics_result = upload_graphics(tuned_model_result)
    assert upload_graphics_result is None  # Assuming it does not return anything

def test_calculated_auc():
    y_true = pd.Series([0, 1, 0, 1])
    y_pred = pd.Series([0.1, 0.8, 0.3, 0.9])
    auc_result = calculated_auc(y_true, y_pred)
    assert isinstance(auc_result, float)

def test_test_evaluated(sample_df):
    best_model = train_model(sample_df)
    df_test = split_datasets(sample_df)[1]
    test_evaluated_result = test_evaluated(best_model, df_test)
    assert test_evaluated_result is None  # Assuming it does not return anything

def test_get_score(sample_df):
    best_model = train_model(sample_df)
    df_test = split_datasets(sample_df)[1]
    get_score_result = get_score(best_model, df_test)
    assert get_score_result is None  # Assuming it does not return anything

def test_run(sample_df, mocker):
    # Mocking mlflow functions for testing
    mocker.patch("mlflow.start_run")
    mocker.patch("mlflow.log_params")
    mocker.patch("mlflow.log_metric")
    mocker.patch("mlflow.end_run")

    run_result = run()
    assert run_result is None  # Assuming it does not return anything
