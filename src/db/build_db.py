from pathlib import Path
import csv

import sqlite3

from src.db.queries import (
    CREATE_COFFEE_BEANS_TABLE,
    CREATE_COFFEE_ROASTER_TABLE,
    INSERT_INTO_BEANS_TABLE,
    INSERT_INTO_ROASTERS_TABLE
)
from src.db.schema import (
    BEANS_TABLE,
    ROASTERS_TABLE
)


def create_db(db_path='data/coffee_canary.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(CREATE_COFFEE_ROASTER_TABLE)
    cursor.execute(CREATE_COFFEE_BEANS_TABLE)
    conn.commit()
    conn.close()


def load_roasters_from_csv(
    csv_path='data/coffee_roasters.csv',
    db_path='data/coffee_canary.db'
):
    if not Path(csv_path).exists():
        print(f"CSV file {csv_path} does not exist.")
        return

    print("loading roasters from csv...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {ROASTERS_TABLE}')

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute(INSERT_INTO_ROASTERS_TABLE, (
                row['name'].strip(),
                row['city'].strip() if row['city'] else None,
                row['state'].strip() if row['state'] else None,
                row['website'].strip() if row['website'] else None
            ))

    conn.commit()
    count = cursor.execute(f'SELECT COUNT(*) FROM {ROASTERS_TABLE}').fetchone()[0]
    conn.close()

    print(f"Loaded roasters into database. Total roasters: {count}")


def load_beans_from_csv(
    csv_path='data/coffee_beans.csv',
    db_path='data/coffee_canary.db'
):
    if not Path(csv_path).exists():
        print(f"CSV file {csv_path} does not exist.")
        return

    print("loading beans from csv...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {BEANS_TABLE}')

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute(INSERT_INTO_BEANS_TABLE, (
                row['purchase_date'].strip() if row['purchase_date'] else None,
                row['roaster'].strip() if row['roaster'] else None,
                row['blend_name'].strip() if row['blend_name'] else None,
                row['roast_level'].strip() if row['roast_level'] else None,
                row['roast_date'].strip() if row['roast_date'] else None,
                float(row['weight_grams']) if row['weight_grams'] else None,
                row['tasting_notes'].strip() if row['tasting_notes'] else None,
                row['origin_country'].strip() if row['origin_country'] else None,
                row['processing_method'].strip() if row['processing_method'] else None
            ))

    conn.commit()
    count = cursor.execute(f'SELECT COUNT(*) FROM {BEANS_TABLE}').fetchone()[0]
    conn.close()

    print(f"Loaded coffee beans into database. Total beans: {count}")


def setup_db_from_csv(
    roasters_csv='data/coffee_roasters.csv',
    beans_csv='data/coffee_beans.csv',
    db_path='data/coffee_canary.db'
):
    create_db()
    try:
        load_roasters_from_csv()
        load_beans_from_csv()
    except Exception as e:
        print(f"Error setting up database: {e}")