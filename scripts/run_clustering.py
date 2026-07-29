"""
Run Company Clustering
N100 Financial Intelligence Platform
"""

from pathlib import Path
import pandas as pd
import sys
from sqlalchemy import create_engine

PROJECT_ROOT=Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))
from src.analytics.clustering import CompanyClustering


# ---------------------------------------------------------
# Directories
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"

OUTPUT_DIR = PROJECT_ROOT / "output"

REPORT_DIR = PROJECT_ROOT / "reports"


# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

companies_df = pd.read_excel(
    DATA_DIR / "raw" / "companies.xlsx",
    header=1,
)


DB_PATH = DATA_DIR / "nifty100.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

financial_ratios_df = pd.read_sql(
    "SELECT * FROM stg_financial_ratios",
    engine,
)



# ---------------------------------------------------------
# Run Clustering
# ---------------------------------------------------------

clustering = CompanyClustering(
    companies_df=companies_df,
    ratios_df=financial_ratios_df,
    output_dir=OUTPUT_DIR,
    reports_dir=REPORT_DIR,
)

cluster_df = clustering.run()


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

print("\n==============================")
print("Company Clustering Completed")
print("==============================")

print(f"Companies clustered : {len(cluster_df)}")
print(f"Clusters created    : {cluster_df['cluster_id'].nunique()}")

print("\nCluster Distribution")
print("-" * 60)

print(cluster_df.groupby(["cluster_id", "cluster_name"]
        ).size().reset_index(name="companies"))
    
print("\nGenerated Files")
print("-" * 60)

print(f"Cluster Labels       : {OUTPUT_DIR / 'cluster_labels.csv'}")
print(f"Cluster Profile      : {OUTPUT_DIR / 'cluster_profile.csv'}")
print(f"Outlier Report       : {OUTPUT_DIR / 'outlier_report.csv'}")
print(f"Portfolio Statistics : {OUTPUT_DIR / 'portfolio_stats.csv'}")
print(f"Correlation Matrix   : {OUTPUT_DIR / 'correlation_matrix.csv'}")

print(f"Elbow Plot           : {REPORT_DIR / 'elbow_plot.png'}")
print(f"Correlation Heatmap  : {REPORT_DIR / 'correlation_heatmap.png'}")

print("\nDone.")