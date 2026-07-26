"""
=========================================================
Valuation Analytics Module
N100 Financial Intelligence Platform
=========================================================

Computes

1. FCF Yield
2. Company 5-Year Median PE
3. Sector Median PE
4. Relative Valuation
5. Valuation Flags

Outputs

output/valuation_summary.xlsx
output/valuation_flags.csv
"""

from pathlib import Path
import logging

import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


class ValuationAnalytics:
    """
    Valuation Analytics Engine
    """

    def __init__(self, output_dir="output"):

        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(

            parents=True,

            exist_ok=True

        )

    # =====================================================
    # Utility Functions
    # =====================================================

    @staticmethod
    def safe_divide(a, b):

        try:

            if pd.isna(a):

                return np.nan

            if pd.isna(b):

                return np.nan

            if b == 0:

                return np.nan

            return a / b

        except Exception:

            return np.nan

    # =====================================================
    # Main Function
    # =====================================================

    def compute(

        self,

        companies_df,

        ratios_df,

        market_cap_df,

        sectors_df

    ):

        logger.info("Starting valuation analytics...")
       
        # -------------------------------------------------
        # Latest Financial Year
        # -------------------------------------------------

        latest_year = ratios_df["year"].max()

        logger.info(

            f"Latest Financial Year : {latest_year}"

        )

        ratios_latest = (

            ratios_df

            [

                ratios_df["year"]

                ==

                latest_year

            ]

            .copy()

        )

        market_latest = (

            market_cap_df

            [

                market_cap_df["year"]

                ==

                latest_year

            ]

            .copy()

        )

        # -------------------------------------------------
        # Company Information
        # -------------------------------------------------

        company_info = companies_df[

            [

                "id",

                "company_name"

            ]

        ].copy()
        company_info.rename(
        columns={"id": "company_id"},
        inplace=True
    )

        # -------------------------------------------------
        # Sector Information
        # -------------------------------------------------

        sector_info = sectors_df[

            [

                "company_id",

                "broad_sector",

                "sub_sector"

            ]

        ].copy()

        # -------------------------------------------------
        # Five-Year PE History
        # -------------------------------------------------

        available_years = sorted(

            ratios_df["year"]

            .dropna()

            .unique()

        )

        five_years = available_years[-5:]

        pe_history = (

            ratios_df

            [

                ratios_df["year"]

                .isin(five_years)

            ]

            [

                [

                    "company_id",

                    "price_to_earnings"

                ]

            ]

            .copy()

        )

        company_pe = (

            pe_history

            .groupby(

                "company_id"

            )["price_to_earnings"]

            .median()

            .reset_index()

        )

        company_pe.rename(

            columns={

                "price_to_earnings":

                "five_year_median_PE"

            },

            inplace=True

        )

        # -------------------------------------------------
        # Merge Data
        # -------------------------------------------------

        valuation = (

            ratios_latest

            .merge(

                market_latest[

                    [

                        "company_id",

                        "market_cap_crore",

                        "pe_ratio",

                        "pb_ratio",

                        "ev_ebitda"

                    ]

                ],

                on="company_id",

                how="left"

            )

            .merge(

                company_info,

                on="company_id",

                how="left"

            )

            .merge(

                sector_info,

                on="company_id",

                how="left"

            )

            .merge(

                company_pe,

                on="company_id",

                how="left"

            )

        )

        logger.info(

            f"Companies Analysed : {len(valuation)}"

        )

        # -------------------------------------------------
        # FCF Yield
        # -------------------------------------------------

        valuation["FCF_yield_pct"] = (

            valuation["free_cash_flow_cr"]

            /

            valuation["market_cap_crore"]

        ) * 100

            # -------------------------------------------------
        # Sector Median PE (Latest Year)
        # -------------------------------------------------

        sector_pe = (

            valuation

            .groupby(

                "broad_sector"

            )["pe_ratio"]

            .median()

            .reset_index()

        )

        sector_pe.rename(

            columns={

                "pe_ratio":

                "sector_median_PE"

            },

            inplace=True

        )

        valuation = valuation.merge(

            sector_pe,

            on="broad_sector",

            how="left"

        )

        # -------------------------------------------------
        # Relative Valuation Metrics
        # -------------------------------------------------

        valuation["PE_vs_5yr_median_pct"] = (

            (

                valuation["pe_ratio"]

                -

                valuation["five_year_median_PE"]

            )

            /

            valuation["five_year_median_PE"]

        ) * 100

        valuation["PE_vs_sector_median_pct"] = (

            (

                valuation["pe_ratio"]

                -

                valuation["sector_median_PE"]

            )

            /

            valuation["sector_median_PE"]

        ) * 100

        valuation.replace(

            [

                np.inf,

                -np.inf

            ],

            np.nan,

            inplace=True

        )

        # -------------------------------------------------
        # Valuation Flags
        # -------------------------------------------------

        def valuation_flag(row):

            pe = row["pe_ratio"]

            median = row["five_year_median_PE"]

            if pd.isna(pe):

                return "Fair"

            if pd.isna(median):

                return "Fair"

            if median <= 0:

                return "Fair"

            if pe >= median * 1.50:

                return "Caution"

            elif pe <= median * 0.70:

                return "Discount"

            return "Fair"

        valuation["flag"] = (

            valuation.apply(

                valuation_flag,

                axis=1

            )

        )

        # -------------------------------------------------
        # Round Numeric Columns
        # -------------------------------------------------

        numeric_cols = [

            "pe_ratio",

            "pb_ratio",

            "ev_ebitda",

            "FCF_yield_pct",

            "five_year_median_PE",

            "sector_median_PE",

            "PE_vs_5yr_median_pct",

            "PE_vs_sector_median_pct"

        ]

        for col in numeric_cols:

            if col in valuation.columns:

                valuation[col] = (

                    valuation[col]

                    .round(2)

                )

        # -------------------------------------------------
        # Final Output
        # -------------------------------------------------

        output = valuation[

            [

                "company_id",

                "company_name",

                "broad_sector",

                "pe_ratio",

                "pb_ratio",

                "ev_ebitda",

                "FCF_yield_pct",

                "five_year_median_PE",

                "sector_median_PE",

                "PE_vs_5yr_median_pct",

                "PE_vs_sector_median_pct",

                "flag"

            ]

        ].copy()

        output.rename(

            columns={

                "broad_sector": "sector",

                "pe_ratio": "P/E",

                "pb_ratio": "P/B",

                "ev_ebitda": "EV/EBITDA",

                "five_year_median_PE": "5yr_median_PE"

            },

            inplace=True

        )

        output.sort_values(

            [

                "sector",

                "company_name"

            ],

            inplace=True

        )

        output.reset_index(

            drop=True,

            inplace=True

        )

        # -------------------------------------------------
        # Export Excel
        # -------------------------------------------------

        summary_file = (

            self.output_dir /

            "valuation_summary.xlsx"

        )

        output.to_excel(

            summary_file,

            index=False

        )

        # -------------------------------------------------
        # Export Flags CSV
        # -------------------------------------------------

        flagged = output[

            output["flag"].isin(

                [

                    "Caution",

                    "Discount"

                ]

            )

        ].copy()

        flags_file = (

            self.output_dir /

            "valuation_flags.csv"

        )

        flagged.to_csv(

            flags_file,

            index=False

        )

        # -------------------------------------------------
        # Logging
        # -------------------------------------------------

        logger.info(

            "=" * 60

        )

        logger.info(

            f"Companies Analysed : {len(output)}"

        )

        logger.info(

            f"Caution : {(output['flag']=='Caution').sum()}"

        )

        logger.info(

            f"Discount : {(output['flag']=='Discount').sum()}"

        )

        logger.info(

            f"Fair : {(output['flag']=='Fair').sum()}"

        )

        logger.info(

            f"Summary saved : {summary_file}"

        )

        logger.info(

            f"Flags saved : {flags_file}"

        )

        logger.info(

            "=" * 60

        )

        return output


# =========================================================
# Standalone Execution
# =========================================================

if __name__ == "__main__":

    print(

        "Valuation Analytics Module Loaded."

    )

    print(

        "Use ValuationAnalytics().compute(...)"

    )