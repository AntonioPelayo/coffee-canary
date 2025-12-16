import dash
from dash import html, dcc

dash.register_page(
    __name__,
    path="/admin_coffee_beans_form",
    name="Admin Coffee Beans Form",
)

FIELD_STYLE = {"width": "300px"}
ROW_STYLE = {"marginBottom": "12px"}
LABEL_STYLE = {
    "display": "block",
    "marginBottom": "4px",
}

layout = html.Div([
    html.H2("Coffee Beans Entry"),

    html.Div([
        html.Label("Purchase Date", style=LABEL_STYLE),
        dcc.DatePickerSingle(id="purchase_date", style=FIELD_STYLE),
    ], style=ROW_STYLE),

    html.Div([
        html.Label("Roaster", style=LABEL_STYLE),
        dcc.Input(id="roaster", type="text", style=FIELD_STYLE),
    ], style=ROW_STYLE),

    html.Div([
        html.Label("Blend Name", style=LABEL_STYLE),
        dcc.Input(id="blend_name", type="text", style=FIELD_STYLE),
    ], style=ROW_STYLE),

    html.Div([
        html.Label("Roast Level", style=LABEL_STYLE),
        dcc.Input(id="roast_level", type="text", style=FIELD_STYLE),
    ], style=ROW_STYLE),

    html.Div([
        html.Label("Roast Date", style=LABEL_STYLE),
        dcc.DatePickerSingle(id="roast_date", style=FIELD_STYLE),
    ], style=ROW_STYLE),

    html.Div([
        html.Label("Weight (grams)", style=LABEL_STYLE),
        dcc.Input(id="weight_grams", type="number", style=FIELD_STYLE),
    ], style=ROW_STYLE),

    html.Div([
        html.Label("Tasting Notes", style=LABEL_STYLE),
        dcc.Textarea(
            id="tasting_notes",
            style={**FIELD_STYLE, "height": "80px"},
        ),
    ], style=ROW_STYLE),

    html.Div([
        html.Label("Origin Country", style=LABEL_STYLE),
        dcc.Input(id="origin_country", type="text", style=FIELD_STYLE),
    ], style=ROW_STYLE),

    html.Div([
        html.Label("Processing Method", style=LABEL_STYLE),
        dcc.Input(id="processing_method", type="text", style=FIELD_STYLE),
    ], style=ROW_STYLE),

    html.Button("Submit", id="submit_beans"),
])
