import pandas as pd
import random 
import sys  
from pathlib import Path 

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from sqlalchemy import create_engine
from config.setting import DB_PATH




engine = create_engine(f"sqlite:///{DB_PATH}")

companies = pd.read_sql(
    "SELECT id FROM stg_companies",
    engine
)

sample_companies = random.sample(
    companies["id"].tolist(),
    5
)

print("Random Companies:")
print(sample_companies)

coverage = pd.read_sql(
    """
    SELECT
        company_id,
        COUNT(DISTINCT year) AS year_count
    FROM stg_profitandloss
    GROUP BY company_id
    ORDER BY year_count
    """,
    engine
)

print(coverage.head(20))

low_coverage = coverage[
    coverage["year_count"] < 5
]

print(low_coverage)

low_coverage.to_csv(
    "output/companies_lt_5_years.csv",
    index=False
)