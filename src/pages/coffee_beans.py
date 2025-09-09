import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.utils.data_helpers import (
    load_beans_dataframe,
    load_roasters_dataframe,
    make_roaster_distribution,
    make_roast_level_pie,
    make_cumulative_weight_line,
    make_roaster_location_map,
)

dash.register_page(__name__, path='/coffee_beans', name='Coffee Beans')

beans_df = load_beans_dataframe()
roasters_df = load_roasters_dataframe()

fig_cumulative_weight = make_cumulative_weight_line(beans_df, roasters_df)
fig_roast_levels = make_roast_level_pie(beans_df)
fig_roaster_map = make_roaster_location_map(beans_df, roasters_df)
fig_roasters = make_roaster_distribution(beans_df, roasters_df)

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Antonio's Coffee Blend Dashboard"), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_cumulative_weight))
    ], className='mt-4'),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_roast_levels)),
        dbc.Col(dcc.Graph(figure=fig_roaster_map))
    ], className='mt-4'),
    dbc.Row([
    ], className='mt-4'),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=fig_roasters), width=12)
    ])
], fluid=True)