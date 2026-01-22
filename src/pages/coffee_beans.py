import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

from src.utils.data_helpers import (
    load_beans_dataframe,
    load_roasters_dataframe,
)
from src.utils import plots

dash.register_page(__name__, path='/coffee_beans', name='Coffee Beans')

beans_df = load_beans_dataframe()
roasters_df = load_roasters_dataframe()

layout = dbc.Container([
    dbc.Row([dbc.Col(
        html.H2("Antonio's Coffee Bean Consumption Dashboard"),
        width=12
    )]),
    dbc.Row([dbc.Col(
        dcc.Graph(figure=plots.make_cumulative_weight_line(beans_df)),
        width=12
    )], className='mt-4'),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=plots.make_roast_level_pie(beans_df))),
        dbc.Col(plots.make_roaster_location_map(roasters_df))
    ], className='mt-4'),
    dbc.Row([dbc.Col(
        dcc.Graph(figure=plots.make_roaster_distribution(beans_df, roasters_df)),
        width=12
    )]),
    dbc.Row([dbc.Col(
        dcc.Graph(figure=plots.make_coffee_notes_distribution(beans_df)),
        width=12
    )])
], fluid=True)