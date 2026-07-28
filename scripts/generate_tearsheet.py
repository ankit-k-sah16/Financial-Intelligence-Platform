"""
Generate Company Tear Sheets
N100 Financial Intelligence Platform
"""

from pathlib import Path
import argparse
import logging

import pandas as pd
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.reports.batch_tearsheets import (
    BatchTearSheetGenerator,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Project Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"

REPORT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR = PROJECT_ROOT / "reports"/"tearsheets"

# ---------------------------------------------------------
# Load Datasets
# ---------------------------------------------------------

def load_data():

    companies = pd.read_excel(
        DATA_DIR / "raw"/"companies.xlsx",header=1,
    )

    profitloss = pd.read_excel(
        DATA_DIR /"raw"/ "profitandloss.xlsx",header=1,
    )

    balancesheet = pd.read_excel(
        DATA_DIR / "raw"/"balancesheet.xlsx",header=1,
    )

    cashflow = pd.read_excel(
        DATA_DIR /"raw"/ "cashflow.xlsx",header=1,
    )

    proscons = pd.read_excel(
        DATA_DIR /"raw"/ "prosandcons.xlsx",header=1,
    )
    sectors = pd.read_excel(
    DATA_DIR / "supporting" / "sectors.xlsx"
)
    intelligence = pd.read_excel(
        REPORT_DIR /
        "cashflow_intelligence.xlsx",
    )

    return (
        companies,
        profitloss,
        balancesheet,
        cashflow,
        proscons,
        intelligence,
        sectors
    )

# ---------------------------------------------------------
# Generator Factory
# ---------------------------------------------------------

def create_generator():

    (
        companies,
        profitloss,
        balancesheet,
        cashflow,
        proscons,
        intelligence,
        sectors,
    ) = load_data()

    return BatchTearSheetGenerator(
        companies_df=companies,
        profitloss_df=profitloss,
        balancesheet_df=balancesheet,
        cashflow_df=cashflow,
        proscons_df=proscons,
        intelligence_df=intelligence,
        sectors_df=sectors,
        output_dir=OUTPUT_DIR,
    )

# ---------------------------------------------------------
# CLI Arguments
# ---------------------------------------------------------

def parse_args():

    parser = argparse.ArgumentParser(
        description="Generate Company Tear Sheets",
    )

    parser.add_argument(
        "--company",
        type=str,
        help="Generate a single company report",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate all company reports",
    )

    parser.add_argument(
        "--companies",
        nargs="+",
        help="Generate selected company reports",
    )

    return parser.parse_args()

# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    args = parse_args()

    generator = create_generator()

    if args.all:

        logger.info(
            "Generating reports for all companies..."
        )

        report = generator.generate_all()

        print(report)

        return

    if args.company:

        generator.generate_company(
            args.company.upper(),
        )

        return

    if args.companies:

        report = generator.generate_selected(
            [c.upper() for c in args.companies]
        )

        print(report)

        return

    print(
        "\nNo option selected.\n"
    )

    print(
        "Examples:\n"
    )

    print(
        "python scripts/generate_tearsheets.py --all"
    )

    print(
        "python scripts/generate_tearsheets.py --company RELIANCE"
    )

    print(
        "python scripts/generate_tearsheets.py --companies TCS INFY HDFCBANK"
    )


if __name__ == "__main__":
    main()