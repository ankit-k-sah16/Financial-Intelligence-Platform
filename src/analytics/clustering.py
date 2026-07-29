"""
Company Clustering Module
N100 Financial Intelligence Platform

Performs KMeans clustering on companies using financial metrics.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from scipy.stats import zscore

class CompanyClustering:
    """
    KMeans based clustering of companies.
    """

    FEATURES = [
        "return_on_equity_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "fcf_cagr_5yr",
        "operating_profit_margin_pct",
    ]

    CLUSTER_NAMES = {
        0: "High Quality Compounders",
        1: "Defensive Dividend Payers",
        2: "Value Cyclicals",
        3: "Distressed / Turnaround",
        4: "Emerging Growth"
    }

    def __init__(
        self,
        companies_df: pd.DataFrame,
        ratios_df: pd.DataFrame,
        output_dir,
        reports_dir,
    ):

        self.companies = companies_df.copy()
        self.ratios = ratios_df.copy()  

        self.output_dir = Path(output_dir)
        self.reports_dir = Path(reports_dir)

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # Prepare Dataset
    # ---------------------------------------------------------

    def _prepare_dataset(self):

        latest = (
            self.ratios
            .sort_values("year")
            .groupby("company_id")
            .tail(1)
        )
       

        df = latest.copy()
        

        # Sector-wise median imputation
        for feature in self.FEATURES:

            sector_median = (
                df.groupby("broad_sector")[feature]
                .transform("median")
            )

            global_median = df[feature].median()

            df[feature] = (
                df[feature]
                .fillna(sector_median)
                .fillna(global_median)
            )

        return df

    # ---------------------------------------------------------
    # Elbow Plot
    # ---------------------------------------------------------

    def _generate_elbow_plot(self, X):

        inertia = []

        for k in range(2, 11):

            model = KMeans(
                n_clusters=k,
                random_state=42,
                n_init=10,
            )

            model.fit(X)

            inertia.append(model.inertia_)

        plt.figure(figsize=(8, 5))

        plt.plot(
            range(2, 11),
            inertia,
            marker="o",
        )
        plt.xticks(range(2,11))
        plt.xlabel("Number of Clusters (k)")
        plt.ylabel("Inertia")
        plt.title("Elbow Method")

        plt.grid(True)

        plt.savefig(
            self.reports_dir / "elbow_plot.png",
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()

        print(
            "\n✓ Elbow plot saved to reports/elbow_plot.png"
        )
        print(
            "Review the plot to confirm that k=5 lies near the elbow."
        )

    #----------------------------------------------------------
    # Profile Clustering
    #----------------------------------------------------------
    def profile_clustering(self,df):

        

        profile = (df.groupby("cluster_id") .agg(
            company_count=("company_id", "count"),

            roe_mean=("return_on_equity_pct", "mean"),
            roe_median=("return_on_equity_pct", "median"),

            debt_mean=("debt_to_equity", "mean"),
            debt_median=("debt_to_equity", "median"),

            revenue_cagr_mean=("revenue_cagr_5yr", "mean"),
            revenue_cagr_median=("revenue_cagr_5yr", "median"),

            fcf_cagr_mean=("fcf_cagr_5yr", "mean"),
            fcf_cagr_median=("fcf_cagr_5yr", "median"),

            op_margin_mean=("operating_profit_margin_pct", "mean"),
            op_margin_median=("operating_profit_margin_pct", "median"),
        ) .round(2)      
    )
        profile.to_csv(self.output_dir/"cluster_profile.csv")

        return profile

    #----------------------------------------------------------
    # Cluster Naming
    #----------------------------------------------------------
    def assign_cluster_name(self,df):
    

        df['cluster_name']=df['cluster_id'].map(self.CLUSTER_NAMES)

        df.to_csv(self.output_dir/"cluster_labels.csv")

        return df

    #----------------------------------------------------------
    # Correlation Heatmap
    #----------------------------------------------------------
    def correlation_heatmap(self,df):

        CORRELATION_FEATURES=[
           "return_on_equity_pct",

            "return_on_capital_employed_pct",

            "return_on_assets_pct",

            "debt_to_equity",

            "interest_coverage",

            "asset_turnover",

            "operating_profit_margin_pct",

            "net_profit_margin_pct",

            "revenue_cagr_5yr",

            "fcf_cagr_5yr"
        ]

        corr = (df[CORRELATION_FEATURES].corr(method='pearson'))
        corr_matrix = corr

        corr_matrix.to_csv("output/correlation_matrix.csv")

        plt.figure(figsize=(12,10))

        sns.heatmap(
            corr,
            annot=True,
            cmap="RdYlGn",
            fmt=".2f",
            square=True
        )

        plt.tight_layout()

        plt.savefig(
            self.reports_dir /"correlation_heatmap.png", dpi=300
            
           
        )
        plt.close()
        return corr_matrix# ---------------------------------------------------------
# Outlier Detection
# ---------------------------------------------------------
    def detect_outliers(self, df):
        KPI_COLUMNS = [
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
            "return_on_assets_pct",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover",
            "operating_profit_margin_pct",
            "net_profit_margin_pct",
            "revenue_cagr_5yr",
            "fcf_cagr_5yr",
        ]

        outlier_rows = []

        # -----------------------------------------------------
        # Process sector-wise
        # -----------------------------------------------------
        for sector, sector_df in df.groupby("broad_sector"):
            sector_df = sector_df.copy()

            for metric in KPI_COLUMNS:

                if metric not in sector_df.columns:
                    continue

                if sector_df[metric].dropna().empty:
                    continue

                if sector_df[metric].std(skipna=True) == 0:
                    sector_df[f"{metric}_z"] = 0

                else:
                    sector_df[f"{metric}_z"] = zscore(
                        sector_df[metric],
                        nan_policy="omit"
                    )

                flagged = sector_df[sector_df[f"{metric}_z"].abs() > 3 ]

                for _, row in flagged.iterrows():

                    outlier_rows.append({
                        "company_id":  row["company_id"],                    
                        "company_name": row.get("company_name", None),
                        "broad_sector":sector,
                        "metric":metric,                     
                        "value": row[metric],
                        "z_score":round(row[f"{metric}_z"], 2),
                    })        

                    

        # -----------------------------------------------------
        # Save report
        # -----------------------------------------------------
        outlier_report = pd.DataFrame(outlier_rows)

        outlier_report.to_csv(self.output_dir / "outlier_report.csv", index=False )

        print(f" Outlier report saved to "
            f"{self.output_dir/'outlier_report.csv'}"
        )

        print(f"Total Outliers Detected : {len(outlier_report)}" )


        return outlier_report
    # ---------------------------------------------------------
    # Portfolio Statistics
    # ---------------------------------------------------------
    def portfolio_statistics(self, df):

        KPI_COLUMNS = [
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
            "return_on_assets_pct",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover",
            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "free_cash_flow_cr",
            "cash_from_operations_cr",
            "fcf_conversion_rate",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "eps_cagr_5yr",
            "fcf_cagr_5yr",
            "market_cap",
            "pe",
            "pb",
            "dividend_yield",
            "composite_quality_score",
        ]

        stats = []

        for metric in KPI_COLUMNS:

           
            if metric not in df.columns:
                continue

            values = df[metric].dropna()

          
            if len(values) == 0:
                continue

            stats.append({
                "metric": metric,

                "count": int(values.count()),

                "minimum": round(values.min(), 2),

                "P10": round(values.quantile(0.10), 2),

                "P25": round(values.quantile(0.25), 2),

                "P50": round(values.quantile(0.50), 2),

                "P75": round(values.quantile(0.75), 2),

                "P90": round(values.quantile(0.90), 2),

                "maximum": round(values.max(), 2),

                "mean": round(values.mean(), 2),

                "std": round(values.std(), 2),
            })

        portfolio_stats = pd.DataFrame(stats)

        portfolio_stats.sort_values(by="metric",inplace=True)
                  
        portfolio_stats.reset_index(drop=True,inplace=True)

        portfolio_stats.to_csv(self.output_dir / "portfolio_stats.csv", index=False)

        print(f" Portfolio statistics saved to "
            f"{self.output_dir / 'portfolio_stats.csv'}")
            
        print( f"KPIs Profiled : {len(portfolio_stats)}" )
       
        return portfolio_stats

    # ---------------------------------------------------------
    # Run Clustering
    # ---------------------------------------------------------

    def run(self):

        df = self._prepare_dataset()

        X = df[self.FEATURES]

        scaler = StandardScaler()

        X_scaled = scaler.fit_transform(X)

        self._generate_elbow_plot(X_scaled)

        model = KMeans(
            n_clusters=5,
            random_state=42,
            n_init=10,
        )

        labels = model.fit_predict(X_scaled)

        distances = np.linalg.norm(
            X_scaled - model.cluster_centers_[labels],
            axis=1,
        )

        result = pd.DataFrame(
            {
                "company_id": df["company_id"],
                "cluster_id": labels,
                "cluster_name": [
                    self.CLUSTER_NAMES[i]
                    for i in labels
                ],
                "distance_from_centroid": distances.round(4),
            }
        )
        clustered_df = df.copy()

        clustered_df["cluster_id"] = labels
        clustered_df["cluster_name"] = (clustered_df["cluster_id"].map(self.CLUSTER_NAMES))
    
        clustered_df["distance_from_centroid"] = distances

        clustered_df = self.assign_cluster_name(clustered_df)

        print(clustered_df.columns.tolist())
        
        self.profile_clustering(clustered_df)

        self.correlation_heatmap(clustered_df)

        self.detect_outliers(clustered_df)

        self.portfolio_statistics(clustered_df)

        result.to_csv(
            self.output_dir / "cluster_labels.csv",
            index=False,
        )
        print("fcf_cagr_5yr" in self.ratios.columns)
        print(
            f"✓ Cluster labels saved to "
            f"{self.output_dir / 'cluster_labels.csv'}"
        )

        return result