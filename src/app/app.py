import dash
import dash_bootstrap_components as dbc
from dash import html

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Coffee Canary"
server = app.server

app.layout = html.Div(
    [
        html.H1("Coffee Canary"),
        html.H2("Your brewing canary: track, alert, improve, and recommend."),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)