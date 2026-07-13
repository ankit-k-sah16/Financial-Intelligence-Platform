"""
Composite Scoring Engine
----------------------------------

Computes:
1. Composite Quality Score (0-100)
2. Sector Relative Score(0-100)

Weightage
-----------------------------------
Profitability : 35%
Cash Quality  : 30%
Growth        : 20%
Leverage      : 15%

"""

import numpy as np
import pandas as pd
from src.screener.normalization import Normalizer

class Composite_Scorer:
    """
    Computes Composite Quality Scores.
    """

    #-------------------------------------
    # Self Normalization
    #-------------------------------------
    @staticmethod
    def normalize(series,inverse=False):
        """
        Min-Max normalize to 0-100
        
        inverse=True when lower is better 
        (Debt/Equity for example).
        """

        s=series.astype(float)
        if s.nunique() <= 1:
            return pd.Series(50, index=s.index)

        minimum=s.min()
        maximum=s.max()

        score=(s - minimum)/ (maximum - minimum)

        if inverse:
            score= 1 - score

        return (score * 100).clip(0,100)
    
    # -------------------------------------------------------
    # Positive Flag
    # -------------------------------------------------------

    @staticmethod
    def positive_flag(series):
        """
        Converts positive values to 100,
        otherwise 0.
        """

        return np.where(series > 0, 100, 0)

    # -------------------------------------------------------
    # Composite Score
    # -------------------------------------------------------

    @classmethod
    def compute(cls, df):

        df = df.copy()

        # ---------------------------------------------------
        # Profitability
        # ---------------------------------------------------

        roe = Normalizer.normalize(df["return_on_equity_pct"])

        roce = cls.normalize(
            df["return_on_capital_employed_pct"]
        )

        npm = cls.normalize(
            df["net_profit_margin_pct"]
        )

        profitability = ( roe * 0.15 +  roce * 0.10 +npm * 0.10 )

        # ---------------------------------------------------
        # Cash Quality
        # ---------------------------------------------------

        fcf = cls.normalize(
            df["free_cash_flow_cr"]
        )

        cfo = cls.normalize(
            df["cfo_quality_score"]
        )

        positive_fcf = cls.positive_flag(
            df["free_cash_flow_cr"]
        )

        cash_quality = ( fcf * 0.15 + cfo * 0.10 + positive_fcf * 0.05 )

        # ---------------------------------------------------
        # Growth
        # ---------------------------------------------------

        revenue = cls.normalize(
            df["revenue_cagr_5yr"]
        )

        pat = cls.normalize(
            df["pat_cagr_5yr"]
        )

        growth = (revenue * 0.10 + pat * 0.10 )

        # ---------------------------------------------------
        # Leverage
        # ---------------------------------------------------

        debt = Normalizer.normalize(df["debt_to_equity"],inverse=True)
    
        icr = cls.normalize(
            df["interest_coverage"]
        )

        leverage = ( debt * 0.10 +  icr * 0.05 )

        # ---------------------------------------------------
        # Final Composite
        # ---------------------------------------------------

        df["composite_quality_score"] = (

            profitability +

            cash_quality +

            growth +

            leverage

        ).round(2)

        return df

    # -------------------------------------------------------
    # Sector Relative Score
    # -------------------------------------------------------

    @classmethod
    def compute_sector_score(cls, df):

        df = df.copy()

        sector_scores = []

        for sector, group in df.groupby("broad_sector"):

            scores = cls.normalize(
                group["composite_quality_score"]
            )

            sector_scores.append(
                pd.Series(scores.values, index=group.index  
                )
            )

        df["sector_relative_score"] = Normalizer.sector_normalize(df,
                value_column="composite_quality_score",
                sector_column="broad_sector")

        return df

    # -------------------------------------------------------
    # Full Pipeline
    # -------------------------------------------------------

    @classmethod
    def run(cls, df):

        df = cls.compute(df)

        df = cls.compute_sector_score(df)

        return df



