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
    dbc.Row(html.H2("Antonio's Coffee Bean Purchase Dashboard")),
    html.Div(
        children=[
            html.H3("Roaster Locations"),
            plots.make_roaster_location_map(roasters_df),
        ],
        style={'width': '75%', 'marginLeft': 'auto', 'marginRight': 'auto'}
    ),
    dbc.Row(
        children=[
            dcc.Graph(
                figure=plots.make_roast_level_pie(beans_df),
                style={'display': 'inline-block', 'width': '48%'}
            ),
            dcc.Graph(
                figure=plots.make_cumulative_weight_line(beans_df),
                style={'display': 'inline-block', 'width': '48%'}
            )
        ]
    ),
    dbc.Row(children=[
        dcc.Graph(
            figure=plots.make_roaster_distribution(beans_df, roasters_df),
            style={'display': 'inline-block', 'width': '48%'}
        ),
    dcc.Graph(
        figure=plots.make_coffee_notes_distribution(beans_df),
        style={'display': 'inline-block', 'width': '48%'}
    )
    ])
], fluid=True)