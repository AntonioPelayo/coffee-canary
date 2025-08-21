import os
from typing import Optional, Tuple, List
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DEFAULT_BAGS_PATH = 'data/coffee_bags.csv'
DEFAULT_ROASTER_LOCATIONS_PATH = 'data/coffee_roasters.csv'

CITY_STATE_LATLON = {
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
    ('Winters', 'CA'): (38.5246, -121.9702),
    ('Portland', 'OR'): (45.5152, -122.6784),
    ('Santa Cruz', 'CA'): (36.9741, -122.0308),
}


def _resolve_path(path_env: Optional[str], default_rel: str) -> str:
    path = path_env or default_rel
    if not os.path.isabs(path):
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
        path = os.path.join(base, path)
    return path


def load_bags_dataframe() -> pd.DataFrame:
    path = _resolve_path(os.getenv('COFFEE_BAGS_CSV'), DEFAULT_BAGS_PATH)
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        return pd.DataFrame()


def load_roaster_locations_dataframe() -> pd.DataFrame:
    path = _resolve_path(os.getenv('ROASTER_LOCATION_CSV'), DEFAULT_ROASTER_LOCATIONS_PATH)
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        return pd.DataFrame()


def make_roaster_distribution(df: pd.DataFrame):
    if 'Roaster' not in df.columns or df.empty:
        return px.bar(title='No data available')
    counts = df['Roaster'].dropna().value_counts().reset_index()
    counts.columns = ['Roaster', 'Count']
    counts = counts.sort_values(['Count', 'Roaster'], ascending=[False, True])
    return px.bar(counts, x='Roaster', y='Count', title='Distribution of Coffee Beans Bought by Coffee Roaster')


def detect_roast_column(df: pd.DataFrame) -> Optional[str]:
    for candidate in ['Roast Level', 'Roast', 'roast_level']:
        if candidate in df.columns:
            return candidate
    return None


def make_roast_level_pie(df: pd.DataFrame):
    col = detect_roast_column(df)
    if not col:
        return px.bar(title='No data available')
    series = df[col].dropna().astype(str).str.strip()
    series = series[series != '']
    if series.empty:
        return px.bar(title='No data available')
    counts = series.value_counts().reset_index()
    counts.columns = ['Roast Level', 'Count']
    fig = px.pie(counts, names='Roast Level', values='Count', title='Roast Level Proportions', hole=0.4)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def make_cumulative_weight_line(df: pd.DataFrame):
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
    if not (date_col and weight_col):
        return px.line(title='No data available')
    hover_cols = [date_col, weight_col]
    for extra in ['Roaster', 'Blend Name']:
        if extra in df.columns and extra not in hover_cols:
            hover_cols.append(extra)
    df_dates = df[hover_cols].copy().dropna(subset=[date_col, weight_col])
    df_dates[date_col] = pd.to_datetime(df_dates[date_col], errors='coerce')
    df_dates = df_dates.dropna(subset=[date_col]).sort_values(date_col)
    df_dates['Cumulative Weight (g)'] = df_dates[weight_col].astype(float).cumsum()
    fig = px.line(
        df_dates,
        x=date_col,
        y='Cumulative Weight (g)',
        title='Cumulative Weight of Beans Consumed Over Time',
        markers=True,
        hover_data={
            'Roaster': True if 'Roaster' in df_dates.columns else False,
            'Blend Name': True if 'Blend Name' in df_dates.columns else False,
            date_col: False,
            weight_col: True,
            'Cumulative Weight (g)': True
        }
    )
    fig.update_layout(xaxis_title='Date', yaxis_title='Cumulative Weight (g)')
    return fig


def make_roaster_location_map(df_bags: pd.DataFrame, df_roasters: pd.DataFrame):
    if df_bags.empty or df_roasters.empty:
        return go.Figure()
    used = set(df_bags['Roaster'].dropna().unique())
    df_r = df_roasters[df_roasters['Roaster'].isin(used)].copy()
    if df_r.empty:
        return go.Figure()
    df_r['Location'] = df_r['City'] + ', ' + df_r['State']
    df_r['lat'] = df_r.apply(lambda r: CITY_STATE_LATLON.get((r['City'], r['State']), (None, None))[0], axis=1)
    df_r['lon'] = df_r.apply(lambda r: CITY_STATE_LATLON.get((r['City'], r['State']), (None, None))[1], axis=1)
    df_r = df_r.dropna(subset=['lat', 'lon'])
    if df_r.empty:
        return go.Figure()
    fig = go.Figure(go.Scattergeo(
        locationmode='USA-states',
        lon=df_r['lon'],
        lat=df_r['lat'],
        text=df_r['Roaster'] + ' (' + df_r['Location'] + ')',
        mode='markers',
        marker=dict(size=10, color='crimson', line=dict(width=1, color='black')),
        hovertext=df_r['Roaster'] + '<br>' + df_r['Location'],
        hoverinfo='text',
    ))
    fig.update_layout(
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
    return fig

__all__ = [
    'load_bags_dataframe',
    'load_roaster_locations_dataframe',
    'make_roaster_distribution',
    'make_roast_level_pie',
    'make_cumulative_weight_line',
    'make_roaster_location_map'
]