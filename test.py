import sqlite3
import pandas as pd
from config.setting import DB_PATH

conn = sqlite3.connect(DB_PATH)

tables = [
    "stg_companies",
    "stg_financial_ratios",
    "stg_market_cap",
    "stg_sectors"
]

for table in tables:
    print("\n" + "="*70)
    print(table)
    print("="*70)

    df = pd.read_sql(
        f"SELECT * FROM {table} LIMIT 2",
        conn
    )

    print(df.columns.tolist())

conn.close()