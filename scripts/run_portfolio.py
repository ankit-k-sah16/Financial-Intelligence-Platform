from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from scripts.generate_tearsheet import create_generator
from src.reports.portfolio_summary import PortfolioSummary


def main():

    batch = create_generator()

    summary = PortfolioSummary(batch.generator)

    output = Path("reports/portfolio/portfolio_summary.pdf")
    output.parent.mkdir(parents=True, exist_ok=True)

    summary.build(output)

    print(f"Portfolio summary saved to {output}")


if __name__ == "__main__":
    main()