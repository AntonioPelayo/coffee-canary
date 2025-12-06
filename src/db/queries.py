import csv

from .schema import (
    BEANS_TABLE,
    BEANS_COL_ID,
    BEANS_COL_PURCHASE_DATE,
    BEANS_COL_ROASTER,
    BEANS_COL_BLEND_NAME,
    BEANS_COL_ROAST_LEVEL,
    BEANS_COL_ROAST_DATE,
    BEANS_COL_WEIGHT_GRAMS,
    BEANS_COL_TASTING_NOTES,
    BEANS_COL_ORIGIN_COUNTRY,
    BEANS_COL_PROCESSING_METHOD,

    ROASTERS_TABLE,
    ROASTERS_COL_ID,
    ROASTERS_COL_NAME,
    ROASTERS_COL_CITY,
    ROASTERS_COL_STATE,
    ROASTERS_COL_WEBSITE
)

CREATE_COFFEE_BEANS_TABLE = f'''
CREATE TABLE IF NOT EXISTS {BEANS_TABLE} (
    {BEANS_COL_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
    {BEANS_COL_PURCHASE_DATE} TEXT,
    {BEANS_COL_ROASTER} TEXT,
    {BEANS_COL_BLEND_NAME} TEXT,
    {BEANS_COL_ROAST_LEVEL} TEXT,
    {BEANS_COL_ROAST_DATE} TEXT,
    {BEANS_COL_WEIGHT_GRAMS} REAL,
    {BEANS_COL_TASTING_NOTES} TEXT,
    {BEANS_COL_ORIGIN_COUNTRY} TEXT,
    {BEANS_COL_PROCESSING_METHOD} TEXT
)
'''

CREATE_COFFEE_ROASTER_TABLE = f'''
CREATE TABLE IF NOT EXISTS {ROASTERS_TABLE} (
    {ROASTERS_COL_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
    {ROASTERS_COL_NAME} TEXT,
    {ROASTERS_COL_CITY} TEXT,
    {ROASTERS_COL_STATE} TEXT,
    {ROASTERS_COL_WEBSITE} TEXT
)
'''


def create_beans_table(conn):
    conn.execute(CREATE_COFFEE_BEANS_TABLE)
    conn.commit()


def create_roasters_table(conn):
    conn.execute(CREATE_COFFEE_ROASTER_TABLE)
    conn.commit()


def seed_table_from_csv(conn, table: str, csv_path: str):
    cursor = conn.cursor()
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader).strip().split(',')

        col_names = ','.join(header)
        placeholders = ','.join('?' for _ in header)

        for row in reader:
            cursor.execute(
                f'INSERT INTO {table} ({col_names}) VALUES ({placeholders})',
                row
            )

    conn.commit()

def preview_table(conn, table: str, limit: int = 5):
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table} LIMIT {limit}')
    return cursor.fetchall()
