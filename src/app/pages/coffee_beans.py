import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os
import plotly.graph_objects as go

dash.register_page(__name__, path='/coffee_beans', name='Coffee Beans')

DATA_PATH = os.getenv('COFFEE_BAGS_CSV')
ROASTER_PATH = os.getenv('ROASTER_LOCATION_CSV')
if not DATA_PATH:
    # Fallback default
    DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../data/coffee_bags.csv'))
elif not os.path.isabs(DATA_PATH):
    # Normalize path relative to project root if it's relative
    DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../', DATA_PATH))

print(f"Loading coffee bags data from: {DATA_PATH}")
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    df = pd.DataFrame()

fig_roasters = px.bar(title='No data available')
fig_roast_levels = px.bar(title='No data available')
fig_cumulative_weight = px.line(title='No data available')
fig_roaster_map = go.Figure()


if not df.empty:
    # --- Roaster location map ---
    roaster_csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../', ROASTER_PATH))
    if os.path.exists(roaster_csv_path):
        df_roasters = pd.read_csv(roaster_csv_path)
        # Only plot roasters that appear in the coffee data
        used_roasters = set(df['Roaster'].dropna().unique())
        df_roasters = df_roasters[df_roasters['Roaster'].isin(used_roasters)]
        df_roasters['Location'] = df_roasters['City'] + ', ' + df_roasters['State']

        # Static lat/lon lookup for your roaster cities
        city_state_to_latlon = {
            ('Vacaville', 'CA'): (38.3566, -121.9877),
            ('Minden', 'NV'): (38.9540, -119.7674),
            ('Sacramento', 'CA'): (38.5816, -121.4944),
            ('Mount Vernon', 'WA'): (48.4212, -122.3341),
            ('San Rafael', 'CA'): (37.9735, -122.5311),
            ('Boise', 'ID'): (43.6150, -116.2023),
            ('Hollywood', 'CA'): (34.0983, -118.3267),
            ('Emeryville', 'CA'): (37.8313, -122.2858),
            ('Berkeley', 'CA'): (37.8715, -122.2730),
            ('Ipswich', 'MA'): (42.6796, -70.8412),
            ('Las Vegas', 'NV'): (36.1699, -115.1398),
            ('Napa', 'CA'): (38.2975, -122.2869),
            ("Winters", "CA"): (38.5246, -121.9702),
            ("Portland", "OR"): (45.5152, -122.6784),
            ("Santa Cruz", "CA"): (36.9741, -122.0308),
        }
        df_roasters['lat'] = df_roasters.apply(lambda row: city_state_to_latlon.get((row['City'], row['State']), (None, None))[0], axis=1)
        df_roasters['lon'] = df_roasters.apply(lambda row: city_state_to_latlon.get((row['City'], row['State']), (None, None))[1], axis=1)
        df_roasters = df_roasters.dropna(subset=['lat', 'lon'])
        fig_roaster_map = go.Figure(go.Scattergeo(
            locationmode='USA-states',
            lon=df_roasters['lon'],
            lat=df_roasters['lat'],
            text=df_roasters['Roaster'] + ' (' + df_roasters['Location'] + ')',
            mode='markers',
            marker=dict(size=10, color='crimson', line=dict(width=1, color='black')),
            hovertext=df_roasters['Roaster'] + '<br>' + df_roasters['Location'],
            hoverinfo='text',
        ))
        fig_roaster_map.update_layout(
            title='Roaster Locations (US)',
            geo=dict(
                scope='usa',
                projection=go.layout.geo.Projection(type='albers usa'),
                showland=True,
                landcolor='rgb(217, 217, 217)',
                subunitcolor='rgb(255, 255, 255)',
                countrycolor='rgb(255, 255, 255)',
                lakecolor='rgb(255, 255, 255)',
                bgcolor='rgba(0,0,0,0)'
            ),
            margin=dict(l=0, r=0, t=40, b=0)
        )
    # --- Roaster distribution ---
    if 'Roaster' in df.columns:
        roaster_counts = df['Roaster'].dropna().value_counts().reset_index()
        roaster_counts.columns = ['Roaster', 'Count']
        roaster_counts = roaster_counts.sort_values(['Count', 'Roaster'], ascending=[False, True])
        fig_roasters = px.bar(roaster_counts, x='Roaster', y='Count', title='Distribution of Coffee Beans Bought by Coffee Roaster')

    # --- Roast level proportions ---
    roast_col = None
    for candidate in ['Roast Level', 'Roast', 'Roast', 'roast_level']:
        if candidate in df.columns:
            roast_col = candidate
            break
    if roast_col:
        roast_series = df[roast_col].dropna().astype(str).str.strip()
        roast_series = roast_series[roast_series != '']
        if not roast_series.empty:
            roast_counts = roast_series.value_counts().reset_index()
            roast_counts.columns = ['Roast Level', 'Count']
            fig_roast_levels = px.pie(roast_counts, names='Roast Level', values='Count', title='Roast Level Proportions', hole=0.4)
            fig_roast_levels.update_traces(textposition='inside', textinfo='percent+label')

    # --- Cumulative weight time series ---
    date_col = None
    for candidate in ['Date', 'date', 'Purchase Date', 'Bought Date']:
        if candidate in df.columns:
            date_col = candidate
            break
    weight_col = None
    for candidate in ['Weight (g)', 'Net Weight (g)', 'Net Weight', 'Weight']:
        if candidate in df.columns:
            weight_col = candidate
            break
    if date_col and weight_col:
        # Parse dates and drop rows with missing/invalid dates or weights
        hover_cols = [date_col, weight_col]
        for extra in ['Roaster', 'Blend Name']:
            if extra in df.columns and extra not in hover_cols:
                hover_cols.append(extra)
        df_dates = df[hover_cols].copy()
        df_dates = df_dates.dropna(subset=[date_col, weight_col])
        df_dates[date_col] = pd.to_datetime(df_dates[date_col], errors='coerce')
        df_dates = df_dates.dropna(subset=[date_col])
        df_dates = df_dates.sort_values(date_col)
        # Cumulative sum
        df_dates['Cumulative Weight (g)'] = df_dates[weight_col].astype(float).cumsum()
        fig_cumulative_weight = px.line(
            df_dates,
            x=date_col,
            y='Cumulative Weight (g)',
            title='Cumulative Weight of Beans Consumed Over Time',
            markers=True,
            hover_data={
                'Roaster': True if 'Roaster' in df_dates.columns else False,
                'Blend Name': True if 'Blend Name' in df_dates.columns else False,
                date_col: False,  # already shown
                weight_col: True,
                'Cumulative Weight (g)': True
            }
        )
        fig_cumulative_weight.update_layout(xaxis_title='Date', yaxis_title='Cumulative Weight (g)')


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
