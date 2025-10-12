import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from .data_helpers import detect_roast_column
from ..config import CITY_STATE_LATLON

def make_roaster_distribution(df_bags: pd.DataFrame, df_roasters: pd.DataFrame):
    if df_bags is None or df_bags.empty:
        return px.bar(title='No coffee bean data available')

    if df_roasters is None or df_roasters.empty:
        return px.bar(title='No roaster data available')


    if 'Roaster' in df_bags.columns:
        series = df_bags['Roaster'].dropna().astype(str).str.strip()
        if series.empty:
            return px.bar(title='No data available')

        counts = series.value_counts().reset_index()
        counts.columns = ['Roaster', 'Count']
        counts = counts.sort_values(['Count', 'Roaster'], ascending=[False, True])

        return px.bar(counts, x='Roaster', y='Count', title='Distribution of Coffee Beans by Roaster')

    if 'roaster_id' in df_bags.columns and not df_roasters.empty and {'id', 'name'}.issubset(df_roasters.columns):
        merged = df_bags.merge(
            df_roasters,
            left_on='roaster_id', right_on='id', how='left', suffixes=("_bean", "_roaster")
        )
        merged['Roaster'] = merged['name_roaster']
        counts = merged['Roaster'].dropna().value_counts().reset_index()
        counts.columns = ['Roaster', 'Count']
        counts['Location'] = merged['city'] + ', ' + merged['state']
        counts = counts.sort_values(['Count', 'Roaster'], ascending=[False, True])

        return px.bar(
            counts,
            x='Roaster',
            y='Count',
            hover_data={'Location': True},
            title='Distribution of Coffee Beans by Roaster'
        )

    return px.bar(title='No data available')


def make_roast_level_pie(df: pd.DataFrame):
    """Pie chart of roast level proportions."""
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


def make_cumulative_weight_line(beans_df: pd.DataFrame, roasters_df: pd.DataFrame):
    date_col = None
    for candidate in ['Date', 'date', 'Purchase Date', 'Bought Date', 'purchase_date']:
        if candidate in beans_df.columns:
            date_col = candidate
            break
    weight_col = None
    for candidate in ['Weight (g)', 'Net Weight (g)', 'Net Weight', 'Weight', 'weight_g']:
        if candidate in beans_df.columns:
            weight_col = candidate
            break
    if not (date_col and weight_col):
        return px.line(title='No data available')
    hover_cols = [date_col, weight_col]
    for extra in ['name', 'Blend Name', 'roaster_id', 'Roaster']:
        if extra in beans_df.columns and extra not in hover_cols:
            hover_cols.append(extra)
    df_dates = beans_df[hover_cols].copy().dropna(subset=[date_col, weight_col])
    df_dates[date_col] = pd.to_datetime(df_dates[date_col], errors='coerce')
    df_dates = df_dates.dropna(subset=[date_col]).sort_values(date_col)
    df_dates['Cumulative Weight (g)'] = df_dates[weight_col].astype(float).cumsum()
    merged = df_dates.copy()
    if 'roaster_id' in df_dates.columns and not roasters_df.empty and {'id', 'name'}.issubset(roasters_df.columns):
        merged = df_dates.merge(roasters_df[['id', 'name']], left_on='roaster_id', right_on='id', how='left', suffixes=("_bean", "_roaster"))
        merged['Roaster'] = merged.get('name_roaster', merged.get('Roaster'))
    # hover labels
    merged['Blend Name'] = merged.get('Blend Name', merged.get('name'))
    if 'Bag Weight (g)' not in merged.columns:
        merged['Bag Weight (g)'] = merged[weight_col]
    fig = px.line(
        merged,
        x=date_col,
        y='Cumulative Weight (g)',
        title='Cumulative Weight of Beans Consumed Over Time',
        markers=True,
        hover_data={
            'Blend Name': 'Blend Name' in merged.columns,
            'Roaster': 'Roaster' in merged.columns,
            date_col: False,
            'Bag Weight (g)': 'Bag Weight (g)' in merged.columns,
            'Cumulative Weight (g)': True
        }
    )
    fig.update_layout(xaxis_title='Date', yaxis_title='Cumulative Weight (g)')
    return fig


def make_roaster_location_map(beans_df: pd.DataFrame, roasters_df: pd.DataFrame):
    if roasters_df is None or roasters_df.empty:
        return go.Figure()
    used = set()
    for col in ['Roaster', 'roaster', 'roaster_id', 'roaster_name']:
        if col in beans_df.columns:
            used = set(beans_df[col].dropna().astype(str).str.strip().unique())
            break
    df_r = roasters_df.copy()

    # if used:
    #     if 'name' in df_r.columns:
    #         df_r = df_r[df_r['id'].isin(used)]

    if df_r.empty:
        return go.Figure()
    if not {'name', 'city', 'state'}.issubset(df_r.columns):
        return go.Figure()
    df_r['Location'] = df_r['city'] + ', ' + df_r['state']
    df_r['lat'] = df_r.apply(lambda r: CITY_STATE_LATLON.get((r['city'], r['state']), (None, None))[0], axis=1)
    df_r['lon'] = df_r.apply(lambda r: CITY_STATE_LATLON.get((r['city'], r['state']), (None, None))[1], axis=1)
    df_r = df_r.dropna(subset=['lat', 'lon'])
    df_r = df_r[df_r['id'].notna()]

    if df_r.empty:
        return go.Figure()

    fig = go.Figure(go.Scattergeo(
        locationmode='USA-states',
        lon=df_r['lon'],
        lat=df_r['lat'],
        text=df_r['name'] + ' (' + df_r['Location'] + ')',
        mode='markers',
        marker=dict(size=10, color='crimson', line=dict(width=1, color='black')),
        hovertext=df_r['name'] + '<br>' + df_r['Location'],
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

