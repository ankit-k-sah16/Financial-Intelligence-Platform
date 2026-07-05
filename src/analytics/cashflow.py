"""
Cash Flow Analytics Module
N100 Financial Intelligence Platform
"""

import pandas as pd


class CashFlowAnalytics:

    # -------------------------------------------------
    # Free Cash Flow
    # -------------------------------------------------

    @staticmethod
    def free_cash_flow(operating_activity, investing_activity):
        """
        Free Cash Flow (FCF)

        Formula:
            FCF = Operating Cash Flow + Investing Cash Flow

        Returns:
            float | None
        """

        if pd.isna(operating_activity) or pd.isna(investing_activity):
            return None

        return round(operating_activity + investing_activity, 2)

    # -------------------------------------------------
    # CFO Quality Score
    # -------------------------------------------------

    @staticmethod
    def cfo_quality_score(cfo_list, pat_list):
        """
        Average CFO/PAT ratio over 5 years.

        Returns:
            (score, label)
        """

        if len(cfo_list) < 5 or len(pat_list) < 5:
            return None, "INSUFFICIENT DATA"

        ratios = []

        for cfo, pat in zip(cfo_list, pat_list):

            if pd.isna(cfo) or pd.isna(pat):
                continue

            if pat == 0:
                continue

            ratios.append(cfo / pat)

        if len(ratios) == 0:
            return None, "NO VALID DATA"

        avg_ratio = sum(ratios) / len(ratios)

        if avg_ratio > 1:
            label = "HIGH QUALITY"

        elif avg_ratio >= 0.5:
            label = "MEDIUM QUALITY"

        else:
            label = "LOW QUALITY / ACCRUAL RISK"

        return round(avg_ratio, 2), label

    # -------------------------------------------------
    # CapEx Intensity
    # -------------------------------------------------

    @staticmethod
    def capex_intensity(investing_activity, sales):
        """
        CapEx Intensity (%)

        Formula:
            |Investing Cash Flow| / Sales × 100
        """

        if pd.isna(investing_activity):
            return None, "NO DATA"

        if pd.isna(sales) or sales == 0:
            return None, "NO DATA"

        capex = (abs(investing_activity) / sales) * 100

        if capex < 5:
            label = "Low"

        elif capex < 15:
            label = "Moderate"

        else:
            label = "High"

        return round(capex, 2), label

    # -------------------------------------------------
    # FCF Conversion Rate
    # -------------------------------------------------

    @staticmethod
    def fcf_conversion_rate(free_cash_flow, operating_profit):
        """
        FCF Conversion Rate (%)

        Formula:
            Free Cash Flow / Operating Profit × 100
        """

        if pd.isna(free_cash_flow):
            return None

        if pd.isna(operating_profit):
            return None

        if operating_profit == 0:
            return None

        return round((free_cash_flow / operating_profit) * 100, 2)

    # -------------------------------------------------
    # Capital Allocation Pattern
    # -------------------------------------------------

    @staticmethod
    def capital_allocation_pattern(cfo, cfi, cff, cfo_pat_ratio=None):

        if pd.isna(cfo) or pd.isna(cfi) or pd.isna(cff):
            return "NO DATA"

        signs = (
            "+" if cfo >= 0 else "-",
            "+" if cfi >= 0 else "-",
            "+" if cff >= 0 else "-"
        )

        if signs == ("+", "-", "-"):

            if cfo_pat_ratio is not None and cfo_pat_ratio > 1:
                return "Shareholder Returns"

            return "Reinvestor"

        elif signs == ("+", "+", "-"):
            return "Liquidating Assets"

        elif signs == ("-", "+", "+"):
            return "Distress Signal"

        elif signs == ("-", "-", "+"):
            return "Growth Funded by Debt"

        elif signs == ("+", "+", "+"):
            return "Cash Accumulator"

        elif signs == ("-", "-", "-"):
            return "Pre-Revenue"

        elif signs == ("+", "-", "+"):
            return "Mixed"

        return "Unknown"

    # -------------------------------------------------
    # Capital Allocation Report
    # -------------------------------------------------

    @staticmethod
    def generate_capital_allocation_report(df, output_file):

        rows = []

        for _, row in df.iterrows():

            cfo = row.get("operating_activity")
            cfi = row.get("investing_activity")
            cff = row.get("financing_activity")

            pattern = CashFlowAnalytics.capital_allocation_pattern(
                cfo,
                cfi,
                cff
            )

            rows.append({

                "company_id": row["company_id"],

                "year": row["year"],

                "cfo_sign": (
                    "+" if pd.notna(cfo) and cfo >= 0 else "-"
                ),

                "cfi_sign": (
                    "+" if pd.notna(cfi) and cfi >= 0 else "-"
                ),

                "cff_sign": (
                    "+" if pd.notna(cff) and cff >= 0 else "-"
                ),

                "pattern_label": pattern

            })

        report = pd.DataFrame(rows)

        report.to_csv(output_file, index=False)

        return report