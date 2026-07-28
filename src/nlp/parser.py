"""
=========================================================
Analysis Text Parser
N100 Financial Intelligence Platform
=========================================================

Parses text fields from analysis.xlsx using regex.

Target Metrics
--------------
1. compounded_sales_growth
2. compounded_profit_growth
3. stock_price_cagr
4. roe

Example Text
------------
10 Years: 21%
5 Years: 18%
3 Years: 15.6%

Regex Pattern
-------------
(r"(\\d+)\\s*Years?:?\\s*([\\d.]+)%")

"""

from pathlib import Path
import logging
import re
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

class AnalysisParser:
    """
    Parser for extracting CAGR and ROE values
    from textual fields in analysis.xlsx.
    """

    def __init__(self, output_dir="output"):

        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(parents=True, exist_ok=True)
            
        self.pattern = re.compile(
            r"(\d+)\s*Years?:?\s*([\d.]+)%",
            flags=re.IGNORECASE
        )

    # -----------------------------------------------------
    # Safe Text
    # -----------------------------------------------------
    @staticmethod
    def safe_text(value):

        if pd.isna(value):
            return ""

        return str(value).strip()

    # -----------------------------------------------------
    # Parse Single Text Block
    # -----------------------------------------------------

    def parse_metric(self,company_id,metric_name,text):
        
        parsed_rows = []

        failed_rows = []

        text = self.safe_text(text)

        if text == "":
            failed_rows.append(
                {
                    "company_id": company_id,
                    "metric_type": metric_name,
                    "raw_text": text,
                    "reason": "Empty Text"
                }
            )

            return parsed_rows, failed_rows

        matches = self.pattern.findall(text)

        if len(matches) == 0:

            failed_rows.append(
                {
                    "company_id": company_id,
                    "metric_type": metric_name,
                    "raw_text": text,
                    "reason": "Regex No Match"
                }
            )

            return parsed_rows, failed_rows

        for period, value in matches:

            parsed_rows.append(

                {
                    "company_id": company_id,
                    "metric_type": metric_name,
                    "period_years": int(period),
                    "value_pct": float(value)
                }
            )
        return parsed_rows, failed_rows

    # -----------------------------------------------------
    # Main Parse Function
    # -----------------------------------------------------
    def parse(self, analysis_df):

        logger.info("Starting Analysis Text Parsing...")
        metric_columns = [
            "compounded_sales_growth",

            "compounded_profit_growth",

            "stock_price_cagr",

            "roe"
        ]

        parsed_records = []

        failed_records = []

        for _, row in analysis_df.iterrows():

            company_id = row["company_id"]

            for metric in metric_columns:

                parsed, failed = self.parse_metric(

                    company_id=company_id,

                    metric_name=metric,

                    text=row.get(metric, "")
                )

                parsed_records.extend(parsed)
                failed_records.extend(failed)

        parsed_df = pd.DataFrame(

            parsed_records,
            columns=[
                "company_id",

                "metric_type",

                "period_years",

                "value_pct"
            ]
        )

        failures_df = pd.DataFrame(

            failed_records,

            columns=[

                "company_id",

                "metric_type",

                "raw_text",

                "reason"

            ]

        )
        logger.info(
            f"Parsed Records : {len(parsed_df)}"
        )

        logger.info(
            f"Parse Failures : {len(failures_df)}"
        )

        # -----------------------------------------------------
        # Save Parsed Output
        # -----------------------------------------------------
        parsed_file = (
            self.output_dir /
            "analysis_parsed.csv"
        )

        parsed_df.to_csv(
            parsed_file,
            index=False
        )

        # -----------------------------------------------------
        # Save Parse Failures
        # -----------------------------------------------------

        failure_file = (
            self.output_dir /
            "parse_failures.csv"
        )

        failures_df.to_csv(
            failure_file,
            index=False
        )

        logger.info(
            f"Parsed file saved : {parsed_file}"
        )

        logger.info(
            f"Failure file saved : {failure_file}"
        )
        return parsed_df, failures_df

    # -----------------------------------------------------
    # Cross Validation
    # -----------------------------------------------------
    def validate_against_ratio_engine(self,parsed_df,ratio_df ):

        logger.info(
            "Starting CAGR Cross Validation..."
        )

        validation = parsed_df.copy()

        validation = validation[
            validation["metric_type"].isin(
                [
                    "compounded_sales_growth",
                    "compounded_profit_growth",
                    "stock_price_cagr"
                ]
            )
        ].copy()

        validation = validation.merge(

            ratio_df[
                [
                    "company_id",
                    "metric_type",
                    "period_years",
                    "computed_value_pct"
                ]
            ],

            on=[
                "company_id",
                "metric_type",
                "period_years"
            ],

            how="left"
        )

        # -----------------------------------------------------
        # Calculate Divergence
        # -----------------------------------------------------
        validation["difference_pct"] = (

            validation["value_pct"]- validation["computed_value_pct"] 
            .abs())

        validation["manual_review"] = np.where(

            validation["difference_pct"] > 5,

            "YES", "NO"
        )

        validation["computed_value_pct"] = (validation["computed_value_pct"]
             .round(2)  
        )

        validation["difference_pct"] = (validation["difference_pct"]
             .round(2)
        )

        # -----------------------------------------------------
        # Export Validation Report
        # -----------------------------------------------------
        validation_file = ( self.output_dir / "cagr_validation.csv" )

        validation.to_csv( validation_file, index=False)

        logger.info(f"CAGR Validation saved : {validation_file}")

        logger.info(f"Manual Review Required : " f"{(validation['manual_review']=='YES').sum()}")

        logger.info("=" * 60)

        return validation    

# =========================================================
# Standalone Execution
# =========================================================
if __name__ == "__main__":

    print("Analysis Parser Module Loaded.")

    print("Use AnalysisParser().parse(...)")
    
    print("Use validate_against_ratio_engine(...)")
    
        