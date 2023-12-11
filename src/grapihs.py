from typing import List, Dict, Union
import shimoku_api_python as shimoku
import pandas as pd
import numpy as np
from pathlib import Path

datasets = Path(__file__).resolve().parent.parent / "datasets"

def indicator(shimoku_client: shimoku.Client, df, order):
    """Creates an indicator in shimoku.

    Args:
        shimoku_client (shimoku.Client): The shimoku client.
        order (int): The order of the indicator.
        title (str): The title of the indicator.
        value (str): The value of the indicator.
        color (str): The color of the indicator.
    """
    data =[
        {
        "description": "Total de clientes a los que se puede hacer una oferta",
        "title": "Positivos",
        "value": df[df["prediction_label"] == 1].shape[0],
        "align": "center",
        },
        {
        "description": "Total de clientes a los que no se puede hacer una oferta",
        "title": "Negativos",
        "value": df[df["prediction_label"] == 0].shape[0],
        "align": "center",
        },
    ]
    shimoku_client.plt.indicator(data=data[0], order=order)
    shimoku_client.plt.indicator(data=data[1], order=order+1)

def create_pie_chart(shimoku_client: shimoku.Client, order: int, df: pd.DataFrame, column: str, title: str):
    """Creates a pie chart in shimoku.

    Args:
        shimoku_client (shimoku.Client): The shimoku client.
        order (int): The order of the pie chart.
        df (pandas.DataFrame): The data of the pie chart.
        column (str): The column of the pie chart.
        title (str): The title of the pie chart.
    """
    data = df["prediction_label"].value_counts().reset_index()
    data = data.replace({0: "Negativos", 1: "Positivos"})
    data = data.rename(columns={"index": "name", "prediction_label": "value"})
    shimoku_client.plt.pie(data=data, names="name", order=order,values="value", title=title)
    
def get_label_columns(table_data: pd.DataFrame) -> Dict:
    low_threshold = table_data["Prediction Score"].quantile(0.25)
    mid_threshold = table_data["Prediction Score"].quantile(0.75)
    return {
        'Prediction Label': {
            '0': '#F86C7D',
            '1': '#001E50',
        },
        'Prediction Score': {
            (0, low_threshold): '#F86C7D',
            (low_threshold, mid_threshold): '#F2BB67',
            (mid_threshold, np.inf): '#001E50',
        },
    }
def create_table(df, shimoku_client: shimoku.Client, order:int, title:str):
    """Creates a table in shimoku.

    Args:
        shimoku_client (shimoku.Client): The shimoku client.
        order (int): The order of the table.
        title (str): The title of the table.
        data (pandas.DataFrame): The data of the table.
    """
    df = df[["id","prediction_label", "prediction_score_1", "duration"]]
    df.dropna(inplace=True, subset=["id"])
    df = df.rename(columns={"prediction_label": "Prediction Label", "prediction_score_1": "Prediction Score", "duration": "Duration"})
    label_columns = get_label_columns(df)
    shimoku_client.plt.table(
        order=order,
        title="Clients and scoring",
        data=df,
        label_columns = label_columns,
    )

def feature_importance_chart(shimoku_client: shimoku.Client, order: int, feature_importance: pd.DataFrame):
    shimoku_client.plt.bar(
        data=feature_importance.sort_values('importance', ascending=False)[:10],
        x='features', y=['importance'], order=order, rows_size=2, cols_size=7,
    )

def page_header(shimoku_client: shimoku.Client, order: int):
    prediction_header = (
        "<head>"
        "<style>"  # Styles title
        ".component-title{height:auto; width:100%; "
        "border-radius:16px; padding:16px;"
        "display:flex; align-items:center;"
        "background-color:var(--chart-C1); color:var(--color-white);}"
        "</style>"
        # Start icons style
        "<style>.big-icon-banner"
        "{width:48px; height: 48px; display: flex;"
        "margin-right: 16px;"
        "justify-content: center;"
        "align-items: center;"
        "background-size: contain;"
        "background-position: center;"
        "background-repeat: no-repeat;"
        "background-image: url('https://uploads-ssl.webflow.com/619f9fe98661d321dc3beec7/63594ccf3f311a98d72faff7_suite-customer-b.svg');}"
        "</style>"
        # End icons style
        "<style>.base-white{color:var(--color-white);}</style>"
        "</head>"  # Styles subtitle
        "<div class='component-title'>"
        "<div class='big-icon-banner'></div>"
        "<div class='text-block'>"
        "<h1>Predictions</h1>"
        "<p class='base-white'>"
        "Lead scoring prediction</p>"
        "</div>"
        "</div>"
    )
    shimoku_client.plt.html(html=prediction_header, order=order)

def distribution_header(shimoku_client: shimoku.Client, order: int):
    distribution_header_html = (
        '<div style="width:100%; height:90px; "><h4>Lead distribution according to % scoring prediction</h4>'
        '<p>Total and disaggregated distribution and porcentage</p></div>'
    )
    shimoku_client.plt.html(html=distribution_header_html, order=order)

def plots(shimoku_client: shimoku.Client):
    df = pd.read_csv(datasets/"predictions"/'offers_with_predictions.csv')
    df_features =  pd.read_csv(datasets/"predictions"/'importance_features.csv')
    shimoku_client.set_menu_path('EDA', 'predictions')
    page_header(shimoku_client, 0)
    indicator(shimoku_client, df, 1)
    distribution_header(shimoku_client, 2)
    create_pie_chart(shimoku_client, 3, df, "Prediction Label", "Prediction label")
    create_table(df, shimoku_client, 4, "Clients and scoring")
    feature_importance_chart(shimoku_client, 5, df_features)
