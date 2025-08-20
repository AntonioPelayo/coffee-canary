import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.title = "Coffee Canary"
server = app.server

# Minimal navbar with links to multipage routes
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Coffee Beans", href="/coffee_beans")),
    ],
    brand="Coffee Canary",
    brand_href="/",
    color="dark",
    dark=True,
    className="mb-3",
)

app.layout = html.Div([
    navbar,
    html.Div(dash.page_container, id="page-container", className="p-3"),
])

if __name__ == "__main__":
    app.run(debug=True)