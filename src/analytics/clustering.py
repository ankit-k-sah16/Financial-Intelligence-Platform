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
        0: "Growth Leaders",
        1: "Stable Compounders",
        2: "Value Opportunities",
        3: "High Risk",
        4: "Turnaround Candidates",
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