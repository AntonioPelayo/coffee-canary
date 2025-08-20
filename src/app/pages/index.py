import dash
from dash import html
import dash_bootstrap_components as dbc

# Register landing page at root
dash.register_page(__name__, path='/', name='Home')

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Coffee Canary', className='display-5 mb-3'),
            html.P('Track and explore your coffee bag collection.', className='lead'),
            dbc.Button('Go to Coffee Beans Dashboard', href='/coffee_beans', color='primary')
        ], width=12)
    ], className='py-5')
], fluid=True)
