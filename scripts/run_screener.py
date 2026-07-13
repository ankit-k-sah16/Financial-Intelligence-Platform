from pathlib import Path
import sys
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import sqlite3
import pandas as pd
from config.setting import DB_PATH
from src.screener.engine import ScreenerEngine
from src.screener.presets import PRESETS
from src.screener.exporter import ScreenerExporter
from src.screener.scoring import Composite_Scorer


# ---------------------------------------
# Load ratios
# ---------------------------------------

conn = sqlite3.connect(DB_PATH)

ratios_df = pd.read_sql(
    "SELECT * FROM stg_financial_ratios",
    conn
)

conn.close()


# ---------------------------------------
# Screener
# ---------------------------------------

engine = ScreenerEngine(
    "config/screener_config.yaml"
)

preset_results = {}

for preset in PRESETS:

    print(f"Running {preset}")

    df = engine.screen_preset(
        ratios_df,
        preset
    )

    df = Composite_Scorer.run(df)

    preset_results[preset] = df


# ---------------------------------------
# Export
# ---------------------------------------

ScreenerExporter.export(
    preset_results,
    PRESETS
)

print()

print("=" * 60)

print("Screener Completed Successfully")

print("=" * 60)