import pandas as pd
from src.analytics.cashflow import CashFlowAnalytics

df=pd.read_excel("data/raw/cashflow.xlsx",header=1)

df.columns=df.columns.str.strip().str.lower().str.replace(" ","_")

CashFlowAnalytics.generate_capital_allocation_report(df,"output/capital_allocation.csv")

print("Capital Allocation Report generated successfully and saved to output/capital_allocation.csv")
