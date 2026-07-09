
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

import sqlite3
import pandas as pd

from src.screener.engine import ScreenerEngine

# ------------------------------------------------------------------
# Database connection
# ------------------------------------------------------------------

DB_PATH = "data/nifty100.db"    # Change this if your database is elsewhere

conn = sqlite3.connect(DB_PATH)

# ------------------------------------------------------------------
# Load financial ratios
# ------------------------------------------------------------------

ratios_df = pd.read_sql(
    "SELECT * FROM stg_financial_ratios",
    conn
)

print("=" * 80)
print(ratios_df.columns.tolist())
print("=" * 80)

conn.close()

# ------------------------------------------------------------------
# Initialize screener
# ------------------------------------------------------------------

engine = ScreenerEngine("config/screener_config.yaml")

PRESETS = [
    "quality_compounder",
    "value_pick",
    "growth_accelerator",
    "dividend_champion",
    "debt_free_blue_chip",
    "turnaround_watch"
]

for preset in PRESETS:

    result = engine.screen_preset(ratios_df, preset)

    print(f"{preset:25} -> {len(result)} companies")