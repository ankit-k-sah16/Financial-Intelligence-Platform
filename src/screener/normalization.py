"""
Normalization Utilities
-----------------------

Provides:

1. P10/P90 Winsorisation
2. Min-Max Scaling (0-100)
3. Inverse Scaling (for metrics where lower is better)
4. Sector-wise Normalization
"""

import numpy as np
import pandas as pd


class Normalizer:
    """
    Utility class for winsorisation and normalization.
    """

    # -----------------------------------------------------
    # Winsorisation
    # -----------------------------------------------------

    @staticmethod
    def winsorize(series, lower=0.10, upper=0.90):
        """
        Clip values between the 10th and 90th percentile.

        Parameters
        ----------
        series : pd.Series
        lower : float
        upper : float

        Returns
        -------
        pd.Series
        """

        s = series.copy()

        s = pd.to_numeric(s, errors="coerce")

        low = s.quantile(lower)

        high = s.quantile(upper)

        return s.clip(lower=low, upper=high)

    # -----------------------------------------------------
    # Min-Max Scaling
    # -----------------------------------------------------

    @staticmethod
    def scale(series):
        """
        Scale values between 0 and 100.
        """

        s = pd.to_numeric(series, errors="coerce")

        minimum = s.min()

        maximum = s.max()

        if pd.isna(minimum) or pd.isna(maximum):

            return pd.Series(50,index=s.index )
           
        if maximum == minimum:

            return pd.Series( 50, index=s.index )
            
        scaled = ((s - minimum) / (maximum - minimum) ) * 100

        return scaled.clip(0, 100)

    # -----------------------------------------------------
    # Inverse Scaling
    # -----------------------------------------------------

    @classmethod
    def inverse_scale(cls, series):
        """
        Lower is better.

        Example:
        Debt/Equity
        P/E
        P/B
        """

        return 100 - cls.scale(series)

    # -----------------------------------------------------
    # Winsorize + Scale
    # -----------------------------------------------------

    @classmethod
    def normalize(cls, series, inverse=False):
        """
        Winsorize first, then scale.
        """

        s = cls.winsorize(series)

        if inverse:

            return cls.inverse_scale(s)

        return cls.scale(s)

    # -----------------------------------------------------
    # Sector Relative Normalization
    # -----------------------------------------------------

    @classmethod
    def sector_normalize(cls, df,value_column,sector_column="broad_sector",inverse=False, ):

        """
        Normalize within each sector.

        Returns
        -------
        pd.Series
        """

        scores = pd.Series( index=df.index,dtype=float )
           
        for sector in df[sector_column].dropna().unique():

            mask = (df[sector_column] == sector)

            subset = df.loc[mask,value_column]
                
            scores.loc[mask] = cls.normalize(subset,
                inverse=inverse   
            )

        return scores.round(2)

    # -----------------------------------------------------
    # Batch Normalization
    # -----------------------------------------------------

    @classmethod
    def normalize_dataframe(cls,df,metrics,inverse_metrics=None,):

        """
        Normalize multiple columns.

        Parameters
        ----------
        metrics : list
            Columns to normalize.

        inverse_metrics : list
            Columns where lower values are better.

        Returns
        -------
        DataFrame
        """

        if inverse_metrics is None:

            inverse_metrics = []

        out = df.copy()

        for col in metrics:

            out[col + "_score"] = cls.normalize(

                out[col],

                inverse=col in inverse_metrics

            )

        return out