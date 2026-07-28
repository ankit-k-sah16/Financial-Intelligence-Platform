from pathlib import Path
import sys
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from config.setting import RAW_DATA_DIR, REPORT_DIR,SUPPORTING_DATA_DIR
from src.reports.portfolio_summary import PortfolioSummary


companies = pd.read_excel(
    RAW_DATA_DIR / "companies.xlsx",
    header=1,
)

sectors = pd.read_excel(
   SUPPORTING_DATA_DIR / "sectors.xlsx"
)

ratios = pd.read_excel(
    SUPPORTING_DATA_DIR/ "financial_ratios.xlsx"
)

summary = PortfolioSummary(
    companies_df=companies,
    sectors_df=sectors,
    ratios_df=ratios,
    output_dir=REPORT_DIR,
)

summary.build(
    REPORT_DIR / "portfolio_summary.pdf"
)

print("Portfolio summary generated successfully.")