import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from src.utils.data_helpers import (
    load_beans_dataframe,
    load_roasters_dataframe,
)
from src.utils.plots import (
    make_roaster_distribution,
    make_roast_level_pie,
    make_cumulative_weight_line,
    make_roaster_location_map
)

dash.register_page(__name__, path='/coffee_beans', name='Coffee Beans')

beans_df = load_beans_dataframe()
roasters_df = load_roasters_dataframe()

layout = dbc.Container([
    dbc.Row([dbc.Col(
        html.H2("Antonio's Coffee Bean Consumption Dashboard"),
        width=12
    )]),
    dbc.Row([dbc.Col(
        dcc.Graph(figure=make_cumulative_weight_line(beans_df)),
        width=12
    )], className='mt-4'),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=make_roast_level_pie(beans_df))),
        dbc.Col(dcc.Graph(figure=make_roaster_location_map(roasters_df)))
    ], className='mt-4'),
    dbc.Row([dbc.Col(
        dcc.Graph(figure=make_roaster_distribution(beans_df, roasters_df)),
        width=12
    )])
], fluid=True)