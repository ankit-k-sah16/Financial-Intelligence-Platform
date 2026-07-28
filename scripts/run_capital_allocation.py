"""
Run Capital Allocation Summary Engine

Sprint 3
N100 Financial Intelligence Platform
"""

from pathlib import Path
import logging
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.analytics.capital_allocation_summary import (
    CapitalAllocationSummary,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = PROJECT_ROOT / "output"
def main():
    engine = CapitalAllocationSummary(

        allocation_file=OUTPUT_DIR / "capital_allocation.csv",

        cashflow_file=OUTPUT_DIR / "cashflow_intelligence.xlsx",

        output_dir=OUTPUT_DIR,

    )

    engine.run()

logger.info("Capital Allocation Summary completed successfully.")

if __name__ == "__main__":
    main()
