import pandas as pd
from pathlib import Path
from ydata_profiling import ProfileReport


FILE_REPORTS = Path(__file__).resolve().parent.parent / "reports"

def create_report(df:pd.DataFrame, name_report:str)->None:
    """Creates a report of the dataset.

    Args:
        df (pandas.DataFrame): The dataset.
        name_report (str): The name of the report.
    """
    profile = ProfileReport(df, title=name_report, explorative=True)
    file_name = name_report + '.html'
    file_path = FILE_REPORTS / file_name
    profile.to_file(file_path)
    return file_path
    
def changes_columns(df:pd.DataFrame)->pd.DataFrame:
    """Changes the names of the columns.

    Args:
        df (pandas.DataFrame): The dataset.

    Returns:
        pandas.DataFrame: The dataset with the new names of the columns.
    """
    comuns = df.columns
    rename = {}
    for com in comuns:
        new_com = com.lower().replace(' ', '_')
        rename[com] = new_com
    df.rename(columns=rename, inplace=True)
    return df


def create_columns_null_values(df:pd.DataFrame)->pd.DataFrame:
    """Creates new columns for the null values of the dataset.
    Args:
        df (pandas.DataFrame): The dataset.
    Output:
        pandas.DataFrame: The dataset with new columns for the null values.
    """
    columns_with_null_values = df.columns[df.isnull().any()].tolist()
    for column in columns_with_null_values:
        name_new_column = column + '_isnull'
        name_new_column = name_new_column.replace(' ', '_')
        df[column + '_isnull'] = df[column].isnull()
    return df


