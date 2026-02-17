import dash
from dash import html

dash.register_page(__name__, path="/brew_tools", name="Brew Tools")

layout = html.Div(
    [
        html.H2("Tools I Use to Brew Coffee"),
        html.Div([
            html.H3("Brewers"),
            html.H4("Espro French Press"),
            html.P([
                "French press started my coffee consumption in college and after breaking a few glass presses, my Abuela thrifted in Davis this Espro for me. ",
                "I didn't weigh my coffee, I didn't time my brews, and I didn't ever enjoy cleaning a french press. ",
                "Back then we also didn't try any fancy beans, just pre-ground Peet's or Starbucks. "
            ]),
            html.H4("Breville Barista Express"),
            html.P([
                "My girlfriend's purchase in 2021 that took us deeper into the hobby. ",
                "Amazing at bringing espresso into the home, but after 5 years I still haven't touched the steam wand. ",
            ]),
            html.H4("Aeropress Original + Fellow Prismo"),
            html.P([
                "I purchased this in November 2025 during my trip to the Philippines after a month of drinking instant coffee and it's been a great brewer. ",
                "And also my go-to for lighter roasts that shouldn't(?) be put in the espresso machine. ",
                "I opted for the Fellow Prismo attachment so that I didn't have to deal with drip issues,.. ",
                "or the acrobatic inverted method. ",
                "I typically use both paper and metal filters combined, the metal allowed for a minimal amount of sediment to get through, ",
                "but is convenient on its own in a pinch. ",
                "Unsure if I'll bring it into the back country over instant or cowboy coffee."
            ]),
        ]),
        html.Div([
            html.H3("Grinders"),
            html.H4("Breville Barista Express Built-in Grinder"),
            html.P("Consistent and extremely relable, we may have accidentally poured water into the grinder instead of the reservoir."),
            html.H4("Fellow Opus"),
            html.P([
                "The Fellow Opus has an amazing range of grind settings and is very consistent ",
                "but is nearly unusable due to retention. ",
                "I can expect nearly 2g of coffee to be retained in the grinder after each use, ",
                "and the only way to dislodge the coffee is to violently shake the machine. "
            ])
        ]),
        html.Div([
            html.H3("Other"),
            html.H4("Fellow Stagg EKG"),
            html.P([
                "A temperature controlled and gooseneck kettle is great. ",
                "I just feel that the thermometer is slow to respond so I have to shake the kettle to update the reading. ",
            ]),
            html.H4("Jetboil Flash"),
            html.P([
                "My first bomb proof camping purchase from 2016. ",
                "I'm eyeing some lighter options, but this hasn't failed me yet. ",
            ])
        ]),
        html.Div([
            html.Div([
                html.Img(src="assets/photos/mt_shasta.jpeg", style={"width": "100%"}),
                html.P("Mt. Shasta")
            ], style={"flex": "1", "padding": "10px"}),
            html.Div([
                html.Img(src="assets/photos/dewey_point.jpeg", style={"width": "100%"}),
                html.P("Dewey Point")
            ], style={"flex": "1", "padding": "10px"}),
            html.Div([
                html.Img(src="assets/photos/brewing_in_yosemite.jpeg", style={"width": "100%"}),
                html.P("Jetboil + Aeropress setup in Yosemite Valley.")
            ], style={"flex": "1", "padding": "10px"})
        ], style={"display": "flex", "flexDirection": "row", "justifyContent": "space-between"})
    ], style={"width": "66%"}
)
