from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
from sklearn.preprocessing import LabelEncoder
from matplotlib import pyplot as plt
import seaborn as sns
from pycaret.classification import *
import pandas as pd
import numpy as np
from pathlib import Path
import mlflow
import os

from dotenv import load_dotenv

load_dotenv()

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:8084"))

datasets = Path(__file__).resolve().parent.parent / "datasets"

def read_dataset() -> pd.DataFrame:
    """Reads the dataset from a given path.

    Args:
        path (str): The path of the dataset.

    Returns:
        pandas.DataFrame: The dataset.
    """
    path = datasets / "processed" / "integrated.csv"
    df = pd.read_csv(path)
    df["duration"] = df["duration"].astype(float)
    return df

def crate_colums(df):
    """Creates columns for the categorical columns.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with binary columns.
    """
    bool_cols = df.columns[df.dtypes == bool].tolist()
    numerical_cols = df.columns[df.dtypes == float].tolist()
    categorical_cols = df.columns[df.dtypes == object].tolist()
    categorical_cols.remove('status')
    return bool_cols, numerical_cols, categorical_cols

def convert_to_categorical(df):
    """Converts the categorical columns to categorical type.
    Pycaret needs a numbers internally to work with categorical columns and convert to ohe.
    that's why we are only going to change the encoding to labelencoding, but pycaret already makes the change
    """
    categorical_uses = ['pain', 'lead_source', "status"]
    values = {}
    for col in categorical_uses:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        values[col] = le.classes_
    return df, values
    

def split_datasets(df):
    """Splits the dataset into train and test.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The train dataset.
        pandas.DataFrame: The test dataset.
    """
    df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)
    return df_train, df_test

def train_model(df_train):
    """Trains the model.

    Args:
        df_train (pandas.DataFrame): The train dataset.

    Returns:
        pandas.DataFrame: The model.
    """
    clf = setup(data=df_train, target='status', session_id=42, log_experiment=True, experiment_name='experiment')
    best_model = compare_models(sort='AUC')
    return best_model

def tuned_model(best_model):
    """Tunes the model.

    Args:
        best_model (pandas.DataFrame): The model.
        df_train (pandas.DataFrame): The train dataset.

    Returns:
        pandas.DataFrame: The tuned model.
    """
    tuned_model = tune_model(best_model)
    return tuned_model

def evaluted_model():
    """Evaluates the model.

    Args:
        tuned_model (pandas.DataFrame): The tuned model.
        df_test (pandas.DataFrame): The test dataset.

    Returns:
        pandas.DataFrame: The evaluated model.
    """
    metrics_to_log = ["AUC", "Accuracy", "Recall", "Prec.", "F1", "Kappa", "MCC"]
    metrics = pull()
    for metric_name in metrics_to_log:
        metric_value = metrics[metric_name].values[0]
        mlflow.log_metric(metric_name, metric_value)

    
def upload_graphics(tuned_model):
    """Uploads the graphics of the model.

    Args:
        tuned_model (pandas.DataFrame): The evaluated model.
    """
    plot_names = [
        'auc', 'pr', 'confusion_matrix', 'feature', 'error',
        'class_report', 'boundary', 'learning', 'vc',
        'dimension', 'calibration', 'manifold'
    ]
    for plot_name in plot_names:
        try:
            plot = plot_model(tuned_model, plot=plot_name, save=True)
            mlflow.log_artifact(plot)
        except Exception as e:
            print(f"Error al guardar la visualización {plot_name}: {str(e)}")

def calculated_auc(y_true, y_pred):
    """Calculates the auc.

    Args:
        y_true (pandas.DataFrame): The real values.
        y_pred (pandas.DataFrame): The predicted values.

    Returns:
        float: The auc.
    """
    fpr, tpr, thresholds = roc_curve(y_true, y_pred)
    return auc(fpr, tpr)


def test_evaluated(best_model, df_test):
    predictions_proba = predict_model(best_model, data=df_test, raw_score=True)
    auc = calculated_auc(predictions_proba['status'], predictions_proba['prediction_score_1'])
    mlflow.log_metric('auc', auc)
    cr = classification_report(predictions_proba['status'], predictions_proba["prediction_label"], output_dict  =True)
    mlflow.log_metric('accuracy', cr.pop('accuracy'))
    for class_or_avg, metrics_dict in cr.items():
        for metric, value in metrics_dict.items():
            mlflow.log_metric(class_or_avg + '_' + metric,value)

def get_score(best_model, df_test):
    predictions_proba = predict_model(best_model, data=df_test, raw_score=True)
    predction_score = predictions_proba['prediction_score_1']
    predction_score.to_csv('score.csv', index=False)
    
def run():
    df = read_dataset()
    df, values = convert_to_categorical(df)
    with mlflow.start_run():
        mlflow.log_params(values)
        df_train, df_test = split_datasets(df)
        best_model = train_model(df_train)
        best_model = tuned_model(best_model)
        evaluted_model()
        test_evaluated(best_model, df_test)
        final_rf = finalize_model(best_model)
        save_model(final_rf, 'model')
        get_score(final_rf, df)
        mlflow.end_run()
    
    