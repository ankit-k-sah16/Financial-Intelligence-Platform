import pandas as pd
import re


class DataNormalizer:

    @staticmethod
    @staticmethod
    def normalize_year(value):

        if pd.isna(value):
            return None

        value = str(value).strip()

        # TTM
        if value.upper() == "TTM":
            return None

        # Mar 2024 / Dec 2012
        match = re.search(r"(20\d{2})", value)

        if match:
            return int(match.group())

        # Mar-13 / Mar-24
        match = re.search(r"-(\d{2})$", value)

        if match:
            return int("20" + match.group(1))

        return None
    @staticmethod
    def normalize_ticker(value):
        """
        RELIANCE.NS -> RELIANCE
        infy.bo -> INFY
        """

        if pd.isna(value):
            return None

        value = str(value).strip().upper()

        value = value.replace(".NS", "")
        value = value.replace(".BO", "")

        return value

    @staticmethod
    def clean_column_names(df):
        """
        Standardize dataframe columns.
        """

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        return df
    
    