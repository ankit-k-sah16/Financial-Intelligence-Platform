"""
=========================================================
Run Valuation Analytics
=========================================================
"""
import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))


import pandas as pd

from src.analytics.valuation import ValuationAnalytics


# =========================================================
# Load Data
# =========================================================

companies = pd.read_excel(
    "data/raw/companies.xlsx",
    header=1
)
companies.rename(
    columns={"id": "company_id"},
    inplace=True
)

financial_ratios = pd.read_excel(
    "data/supporting/financial_ratios.xlsx",
    header=0
)

market_cap = pd.read_excel(
    "data/supporting/market_cap.xlsx",
    header=0
)

sectors = pd.read_excel(
    "data/supporting/sectors.xlsx",
    header=0
)

# =========================================================
# Standardize Company Key
# =========================================================

# companies.xlsx uses 'id' whereas the other files use
# 'company_id'. Convert once here.

if "company_id" not in companies.columns:

    companies = companies.rename(
        columns={
            "id": "company_id"
        }
    )

# =========================================================
# Run Analytics
# =========================================================

valuation = ValuationAnalytics(
    output_dir="output"
)

summary = valuation.compute(
    companies_df=companies,
    ratios_df=financial_ratios,
    market_cap_df=market_cap,
    sectors_df=sectors
)

print(summary.head())

print("\nValuation Analytics Completed Successfully.")