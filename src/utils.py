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
    file_path = FILE_REPORTS / name_report + '.html'
    profile.to_file(file_path)
    