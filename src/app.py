import os
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from src.db.build_db import setup_db_from_csv

setup_db_from_csv()
app = dash.Dash(
    __name__,
    use_pages=True,
)
app.title = "Coffee Canary"
server = app.server

navbar = html.Nav([
    html.A(
        "Antonio's Website Home",
        href="https://apelayo.com",
        style={"marginRight": "1rem"}
    ),
    html.A(
        "Antonio's Projects",
        href="https://apelayo.com/projects",
        style={"marginRight": "1rem"}
    ),
    html.A(
        "Coffee Dashboard Home",
        href="/",
        style={"marginRight": "1rem"}
    ),
    html.A(
        "Coffee Purchase Trends",
        href="/coffee_beans",
        style={"marginRight": "1rem"}
    ),
])

app.layout = html.Div([
    navbar,
    html.Div(dash.page_container, id="page-container", className="p-3"),
])

if __name__ == "__main__":
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 8050)),
        debug=os.getenv('DEBUG', 'False') == 'True'
    )
