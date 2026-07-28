"""
Run Cash Flow Intelligence Engine

N100 Financial Intelligence Platform
"""

from pathlib import Path
import logging
import pandas as pd

import sys 
PROJECT_ROOT=Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.analytics.cashflow_kpis import CashFlowIntelligence

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------
# Paths
# ---------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

SUPPORTING_DATA_DIR = PROJECT_ROOT / "data" / "supporting"
OUTPUT_DIR = PROJECT_ROOT / "output"


# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

logger.info("Loading datasets...")

companies_df = pd.read_excel(
    RAW_DATA_DIR / "companies.xlsx",header=1
)


cashflow_df = pd.read_excel(
    RAW_DATA_DIR / "cashflow.xlsx",header=1
)

profitloss_df = pd.read_excel(
    RAW_DATA_DIR / "profitandloss.xlsx",header=1
)

balancesheet_df = pd.read_excel(
    RAW_DATA_DIR / "balancesheet.xlsx",header=1
)

sectors_df = pd.read_excel(
    SUPPORTING_DATA_DIR / "sectors.xlsx"
)

# ---------------------------------------------------
# Run Engine
# ---------------------------------------------------
def main(): 
    engine = CashFlowIntelligence(

        companies_df=companies_df,

        cashflow_df=cashflow_df,

        profitloss_df=profitloss_df,

        balancesheet_df=balancesheet_df,

        sectors_df=sectors_df,
        
        output_dir=OUTPUT_DIR,

    )

    engine._generate_outputs()

logger.info("Cash Flow Intelligence completed successfully.")

if __name__ == "__main__":
    main()