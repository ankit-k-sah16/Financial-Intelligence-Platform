"""
Peer Group Analytics
--------------------

Computes percentile rankings within each peer group.

Output Table:
-------------
peer_percentiles

Columns
-------
company_id
peer_group_name
metric
value
percentile_rank
year
"""

from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine

from config.setting import DB_PATH


class PeerAnalytics:

    def __init__(self):

        self.engine = create_engine(f"sqlite:///{DB_PATH}")

    # ---------------------------------------------------------
    # Load Data
    # ---------------------------------------------------------
    def load_data(self):

        self.ratios = pd.read_sql(
            "SELECT * FROM stg_financial_ratios",
            self.engine
        )

        self.peers = pd.read_sql(
            "SELECT * FROM stg_peer_groups",
            self.engine
        )

        print("Peer Analytics tables loaded.")

    # ---------------------------------------------------------
    # Merge
    # ---------------------------------------------------------
    def merge(self):

        self.df = self.ratios.merge(self.peers, on="company_id",how="left" )

        print(f"Merged Rows : {len(self.df)}")
        
    # --------------------------------------------------------
    # Percentile Rank
    # ---------------------------------------------------------
    @staticmethod
    def percentile(series):

        return series.rank(pct=True, method="average")

    # ---------------------------------------------------------
    # Compute
    # ---------------------------------------------------------
    def compute(self):

        metrics = {

            "ROE":"return_on_equity_pct",
                
            "ROCE": "return_on_capital_employed_pct",
               
            "Net Profit Margin":"net_profit_margin_pct",
                
            "Debt To Equity":"debt_to_equity",                

            "Free Cash Flow": "free_cash_flow_cr",              

            "PAT CAGR 5yr":"pat_cagr_5yr",             

            "Revenue CAGR 5yr":"revenue_cagr_5yr",
                
            "EPS CAGR 5yr":"eps_cagr_5yr",
                
            "Interest Coverage":"interest_coverage",
                
            "Asset Turnover":"asset_turnover"            
        }
        results = []

        groups = self.df.groupby(
            "peer_group_name"
        )

        for (group_name, year), group in self.df.groupby(["peer_group_name", "year"]):

            if pd.isna(group_name):

                print("No peer group assigned.")
                                
                continue

            for metric_name, column in metrics.items():

                if column not in group.columns:
                    continue

                ranks = self.percentile(group[column])
                
                # Lower Debt/Equity is better
                if column == "debt_to_equity":

                    ranks = 1 - ranks

                for idx, row in group.iterrows():

                    results.append({

                        "company_id":row["company_id"],

                        "peer_group_name":group_name,
                            
                        "metric": metric_name,
                           
                        "value":row[column],
                            
                        "percentile_rank":round(ranks.loc[idx],  4  ),
                                                                                                       
                        "year": row["year"]                          
                    })
        self.results = pd.DataFrame(results)

        print()

        print("=" * 60)

        print("Peer Percentiles Computed")

        print(len(self.results))

        print("=" * 60)

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------
    def save(self):

        self.results.to_sql( "peer_percentiles",
            self.engine,
            if_exists="replace",
            index=False
        )           
        print()

        print("=" * 60)

        print("peer_percentiles table updated.")

        print("=" * 60)

    # ---------------------------------------------------------
    # Run
    # ---------------------------------------------------------
    def run(self):

        self.load_data()

        self.merge()

        self.compute()

        self.save()