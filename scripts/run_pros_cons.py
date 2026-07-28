"""
Run Pros & Cons Generation

N100 Financial Intelligence Platform
"""

import logging
from pathlib import Path
import sys 
PROJECT_ROOT=Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import pandas as pd
from config.setting import (
    RAW_DATA_DIR,
    SUPPORTING_DATA_DIR,
    OUTPUT_DIR,
)
from src.nlp.pros_cons_generator import ProsConsGenerator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

def load_excel(file_path,header=0):
    """
    Load an Excel file.
    Returns
    -------
    DataFrame
    """
    logger.info(f"Loading {file_path.name}")
    return pd.read_excel(file_path,header=header )

def load_csv(file_path):
    """
    Load a CSV file.

    Returns
    -------
    DataFrame
    """
    logger.info(f"Loading {file_path.name}")
    return pd.read_csv(file_path)

def main():

    logger.info("=" * 70)
    logger.info("Pros & Cons Generation Started")
    logger.info("=" * 70)

    # -----------------------------
    # Core datasets
    # -----------------------------
    companies_df = load_excel(
        RAW_DATA_DIR / "companies.xlsx",header=1
    )
    companies_df.rename(columns={"id": "company_id"  },inplace=True)  

    balancesheet_df = load_excel(
    RAW_DATA_DIR / "balancesheet.xlsx",
    header=1)

    profitloss_df = load_excel(
    RAW_DATA_DIR / "profitandloss.xlsx",
    header=1)

    cashflow_df = load_excel(
    RAW_DATA_DIR / "cashflow.xlsx",
    header=1)

    # -----------------------------
    # Supporting datasets
    # -----------------------------
    ratios_df = load_excel(
    SUPPORTING_DATA_DIR / "financial_ratios.xlsx",
    header=0
)
    print(ratios_df.columns.tolist())

    market_cap_df = load_excel(
        SUPPORTING_DATA_DIR / "market_cap.xlsx",
        header=0
)
    # -----------------------------
    # Valuation outputs
    # -----------------------------
    valuation_summary_df = load_csv(
        OUTPUT_DIR / "valuation_summary.csv"
    )

    valuation_flag_df = load_csv(
        OUTPUT_DIR / "valuation_flags.csv"
    )
  
    # -----------------------------
    # Generate Pros & Cons
    # -----------------------------

    generator = ProsConsGenerator()

    result = generator.generate(
        companies_df=companies_df,
        ratios_df=ratios_df,
        balancesheet_df=balancesheet_df,
        profitloss_df=profitloss_df,
        cashflow_df=cashflow_df,
        market_cap_df=market_cap_df,
        valuation_summary_df=valuation_summary_df,
        valuation_flag_df=valuation_flag_df,
    )

    # -----------------------------
    # Save output
    # -----------------------------
    output_file = OUTPUT_DIR / "pros_cons_generated.csv"

    result.to_csv(
        output_file,
        index=False,
    )

    logger.info(f"Saved output to {output_file}")
    logger.info(f"Generated {len(result)} records")

    logger.info("=" * 70)
    logger.info("Pros & Cons Generation Completed")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()