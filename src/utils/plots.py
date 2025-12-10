import dash_leaflet as dl
import plotly.express as px
import pandas as pd

from ..db.schema import (
    BEANS_COL_PURCHASE_DATE,
    BEANS_COL_ROASTER,
    BEANS_COL_BLEND_NAME,
    BEANS_COL_ROAST_LEVEL,
    BEANS_COL_WEIGHT_GRAMS,
    ROASTERS_COL_NAME,
    ROASTERS_COL_CITY,
    ROASTERS_COL_STATE,
    ROASTERS_COL_LAT,
    ROASTERS_COL_LON
)
from .google_maps_api import geocode_location

def make_roaster_distribution(beans_df: pd.DataFrame, roasters_df: pd.DataFrame):
    if beans_df is None or beans_df.empty:
        return px.bar(title='No coffee bean data available')

    if roasters_df is None or roasters_df.empty:
        return px.bar(title='No roaster data available')

    roaster_series = beans_df[BEANS_COL_ROASTER].dropna().astype(str).str.strip()
    if roaster_series.empty:
        return px.bar(title='No data available')

    counts = roaster_series.value_counts().reset_index()
    counts.columns = ['Roaster', 'Count']
    counts = counts.sort_values(['Count', 'Roaster'], ascending=[False, True])

    merged = counts.merge(
        roasters_df,
        left_on='Roaster',
        right_on=ROASTERS_COL_NAME,
        how='left'
    )

    merged['Location'] = merged[ROASTERS_COL_CITY] + ', ' + merged[ROASTERS_COL_STATE]

    return px.bar(
        merged,
        x='Roaster',
        y='Count',
        hover_data={'Location': True},
        title='Distribution of Coffee Beans by Roaster'
    )


def make_roast_level_pie(beans_df: pd.DataFrame):
    """Pie chart of roast level proportions."""
    roast_level_series = beans_df[BEANS_COL_ROAST_LEVEL].dropna().astype(str).str.strip()

    if roast_level_series.empty:
        return px.bar(title='No data available')

    counts = roast_level_series.value_counts().reset_index()
    counts.columns = ['Roast Level', 'Count']
    fig = px.pie(
        counts,
        names='Roast Level',
        values='Count',
        title='Roast Level Proportions',
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig


def make_cumulative_weight_line(beans_df: pd.DataFrame):
    if beans_df is None or beans_df.empty:
        return px.line(title='No coffee bean data available')

    col_labels = {
        BEANS_COL_PURCHASE_DATE: 'Purchase Date',
        BEANS_COL_ROASTER: 'Roaster',
        BEANS_COL_BLEND_NAME: 'Blend Name',
        BEANS_COL_WEIGHT_GRAMS: 'Bag Weight (g)',
        'cumulative_weight_g': 'Cumulative Weight (g)',
    }
    df = beans_df.copy()
    df[BEANS_COL_PURCHASE_DATE] = pd.to_datetime(df[BEANS_COL_PURCHASE_DATE], errors='coerce')
    df = df.dropna(subset=[BEANS_COL_PURCHASE_DATE]).sort_values(BEANS_COL_PURCHASE_DATE)
    df['cumulative_weight_g'] = df[BEANS_COL_WEIGHT_GRAMS].astype(float).cumsum()

    fig = px.line(
        df,
        x=BEANS_COL_PURCHASE_DATE,
        y='cumulative_weight_g',
        labels=col_labels,
        title='Cumulative Weight of Beans Consumed Over Time',
        markers=True,
        hover_data={
            BEANS_COL_ROASTER: True,
            BEANS_COL_BLEND_NAME: True,
            BEANS_COL_WEIGHT_GRAMS: True
        }
    )
    fig.update_layout(xaxis_title='Date', yaxis_title='Cumulative Weight (g)')
    return fig


def make_roaster_location_map(roasters_df: pd.DataFrame):
    map = dl.Map(
        [dl.TileLayer(), dl.LocateControl()],
        center=[39.5, -98.35],
        zoom=4,
        style={"height": "50vh", "width": "100%"}
    )
    if roasters_df is None or roasters_df.empty:
        return map

    df = roasters_df.copy()
    df['location'] = df[ROASTERS_COL_CITY] + ", " + df[ROASTERS_COL_STATE]
    df[ROASTERS_COL_LAT], df[ROASTERS_COL_LON] = zip(*df['location'].apply(geocode_location))
    df = df.dropna(subset=[ROASTERS_COL_LAT, ROASTERS_COL_LON])
    if df.empty:
        return map

    markers = []
    for _, row in df.iterrows():
        tooltip_text = f"Roaster: {row[ROASTERS_COL_NAME]}<br>Location: {row['location']}"
        marker = dl.Marker(
            position=[row[ROASTERS_COL_LAT], row[ROASTERS_COL_LON]],
            children=[dl.Tooltip(content=tooltip_text)]
        )
        markers.append(marker)

    map.children.append(dl.LayerGroup(markers))
    return map
