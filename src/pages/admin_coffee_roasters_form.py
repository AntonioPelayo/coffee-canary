import dash
from dash import html, dcc

dash.register_page(
    __name__,
    path="/admin_coffee_roasters_form",
    name="Admin Coffee Roasters Form",
)

FIELD_STYLE = {"width": "300px"}
ROW_STYLE = {"marginBottom": "12px"}
LABEL_STYLE = {
    "display": "block",
    "marginBottom": "4px",
}

layout = html.Div([
    html.H2("Coffee Roasters Entry"),
    html.Div([
        html.Label("Name", style=LABEL_STYLE),
        dcc.Input(id="name", type="text", style=FIELD_STYLE),
    ], style=ROW_STYLE),

    html.Div([
        html.Label("City", style=LABEL_STYLE),
        dcc.Input(id="city", type="text", style=FIELD_STYLE),
    ], style=ROW_STYLE),

    html.Div([
        html.Label("State", style=LABEL_STYLE),
        dcc.Input(id="state", type="text", style=FIELD_STYLE),
    ], style=ROW_STYLE),

    html.Div([
        html.Label("Country", style=LABEL_STYLE),
        dcc.Input(id="country", type="text", style=FIELD_STYLE),
    ], style=ROW_STYLE),

    html.Div([
        html.Label("Website", style=LABEL_STYLE),
        dcc.Input(id="website", type="text", style=FIELD_STYLE),
    ], style=ROW_STYLE),

    html.Button("Submit", id="submit_beans"),
])
