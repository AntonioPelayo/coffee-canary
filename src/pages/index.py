import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='Home')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Coffee Canary', className='display-5 mb-3'),
            html.P('Explore my coffee bean purchase trends and preferences.', className='lead'),
            dbc.Button('Go to Purchase Dashboard', href='/coffee_beans', color='primary')
        ], width=12)
    ], className='py-5')
], fluid=True)
