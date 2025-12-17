import os
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
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Coffee Bag Purchases", href="/coffee_beans")),
        # dbc.NavItem(dbc.NavLink("Daily Consumption", href="/daily_consumption")),
        dbc.DropdownMenu(
            label="Admin Forms",
            nav=True,
            in_navbar=True,
            children=[
                dbc.DropdownMenuItem(
                    "Coffee Beans Form",
                    href="/admin_coffee_beans_form"
                ),
                dbc.DropdownMenuItem(
                    "Coffee Roasters Form",
                    href="/admin_coffee_roasters_form"
                )
            ]
        )
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
    app.run(
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 8050)),
        debug=os.getenv('DEBUG', 'False') == 'True'
    )
