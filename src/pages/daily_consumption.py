import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.utils.data_helpers import (
    load_beans_dataframe,
    load_roasters_dataframe,
)

dash.register_page(__name__, path="/daily_consumption", name="Daily Consumption")



layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Antonio's Daily Coffee Consumption Trends"), width=12)
    ]),
], fluid=True)