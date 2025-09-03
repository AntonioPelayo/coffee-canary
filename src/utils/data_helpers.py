import os
from typing import Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

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


def _get_engine() -> Optional[Engine]:
    """Create a SQLAlchemy engine from environment variables if configured.

    Returns None if insufficient configuration.
    """
    db_url = os.getenv('DB_URL')
    if not db_url:
        host = os.getenv('DB_HOST')
        database = os.getenv('DB_NAME')
        user = os.getenv('DB_USERNAME')
        password = os.getenv('DB_PASSWORD')
        port = os.getenv('DB_PORT', '5432')
        if all([host, database, user, password]):
            db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    if not db_url:
        return None
    try:
        engine = create_engine(db_url, pool_pre_ping=True)
        return engine
    except Exception:
        return None


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Make column names consistent with expected capitalized forms used in charts."""
    if df.empty:
        return df
    rename_map = {}
    for col in df.columns:
        lower = col.lower()
        if lower == 'roast_level':
            rename_map[col] = "Roast Level"
        # if lower.startswith('blend') and col != 'Blend Name':
        #     rename_map[col] = 'Blend Name'
        # if lower in ('weight (g)', 'net weight (g)', 'net weight', 'weight') and col != 'Weight (g)':
        #     rename_map[col] = 'Weight (g)'
    if rename_map:
        df = df.rename(columns=rename_map)
    return df


def load_beans_dataframe() -> pd.DataFrame:
    """Load coffee bean records from Postgres if available, otherwise CSV.

    Table name can be set via COFFEE_BEANS_TABLE (defaults to coffee_beans).
    CSV fallback path via COFFEE_BEANS_CSV.
    """
    engine = _get_engine()
    if engine is not None:
        table = os.getenv('COFFEE_BEANS_TABLE')
        if table:
            query = f'SELECT * FROM {table}'
            try:
                df = pd.read_sql(query, con=engine)
                return df
            except Exception as e:
                print(e)
    # CSV fallback
    csv_path = os.getenv('COFFEE_BEANS_CSV', 'data/coffee_beans.csv')
    try:
        if csv_path and os.path.exists(csv_path):
            return pd.read_csv(csv_path)
    except Exception as e:
        print(e)
    return pd.DataFrame()


def load_roasters_dataframe() -> pd.DataFrame:
    """Load roaster location records from Postgres if available, otherwise CSV."""
    engine = _get_engine()
    if engine is not None:
        table = os.getenv('COFFEE_ROASTERS_TABLE')
        if table:
            query = f'SELECT * FROM {table}'
            try:
                df = pd.read_sql(query, con=engine)
                return df
            except Exception as e:
                print(e)
    # CSV fallback
    csv_path = os.getenv('COFFEE_ROASTERS_CSV', 'data/coffee_roasters.csv')
    try:
        if csv_path and os.path.exists(csv_path):
            return pd.read_csv(csv_path)
    except Exception as e:
        print(e)
    return pd.DataFrame()


def make_roaster_distribution(df_bags: pd.DataFrame, df_roasters: pd.DataFrame):
    if df_bags is None or df_bags.empty:
        return px.bar(title='No data available')
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
            df_roasters[['id', 'name']],
            left_on='roaster_id', right_on='id', how='left', suffixes=("_bean", "_roaster")
        )
        merged['Roaster'] = merged['name_roaster']
        counts = merged['Roaster'].dropna().value_counts().reset_index()
        counts.columns = ['Roaster', 'Count']
        counts = counts.sort_values(['Count', 'Roaster'], ascending=[False, True])
        return px.bar(counts, x='Roaster', y='Count', title='Distribution of Coffee Beans by Roaster')
    return px.bar(title='No data available')


def detect_roast_column(df: pd.DataFrame) -> Optional[str]:
    for candidate in ['Roast Level', 'Roast', 'roast_level']:
        if candidate in df.columns:
            return candidate
    return None


def make_roast_level_pie(df: pd.DataFrame):
    """
    Create a pie chart of roast level proportions.

    df: DataFrame containing coffee bean data
    """
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
    for col in ['Roaster', 'roaster', 'roaster_name', 'name']:
        if col in beans_df.columns:
            used = set(beans_df[col].dropna().astype(str).str.strip().unique())
            break
    df_r = roasters_df.copy()
    if used:
        if 'name' in df_r.columns:
            df_r = df_r[df_r['name'].isin(used)]
    if df_r.empty:
        return go.Figure()
    if not {'name', 'city', 'state'}.issubset(df_r.columns):
        return go.Figure()
    df_r['Location'] = df_r['city'] + ', ' + df_r['state']
    df_r['lat'] = df_r.apply(lambda r: CITY_STATE_LATLON.get((r['city'], r['state']), (None, None))[0], axis=1)
    df_r['lon'] = df_r.apply(lambda r: CITY_STATE_LATLON.get((r['city'], r['state']), (None, None))[1], axis=1)
    df_r = df_r.dropna(subset=['lat', 'lon'])
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

__all__ = [
    'load_beans_dataframe',
    'load_roasters_dataframe',
    'make_roaster_distribution',
    'make_roast_level_pie',
    'make_cumulative_weight_line',
    'make_roaster_location_map'
]