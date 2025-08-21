import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.app.utils.data_helpers import (
    load_bags_dataframe,
    load_roaster_locations_dataframe,
    make_roaster_distribution,
    make_roast_level_pie,
    make_cumulative_weight_line,
    make_roaster_location_map,
)

dash.register_page(__name__, path='/coffee_beans', name='Coffee Beans')

df = load_bags_dataframe()
df_roaster_locations = load_roaster_locations_dataframe()

fig_roasters = make_roaster_distribution(df)
fig_roast_levels = make_roast_level_pie(df)
fig_cumulative_weight = make_cumulative_weight_line(df)
fig_roaster_map = make_roaster_location_map(df, df_roaster_locations)

layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2('Coffee Beans Dashboard'), width=12)
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