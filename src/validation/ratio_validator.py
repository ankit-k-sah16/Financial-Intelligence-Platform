"""
Ratio validation utilities.

Compares calculated financial ratios against values stored
in the source dataset and reports any mismatches.
"""

from src.analytics.ratios import FinancialRatios


class RatioValidator:
    """
    Validate calculated financial ratios against
    source dataset values.
    """

    @staticmethod
    def validate_operating_profit_margin(
        operating_profit,
        sales,
        stored_opm,
        tolerance=1.0
    ):
        """
        Validate Operating Profit Margin.

        Parameters
        ----------
        operating_profit : float

        sales : float

        stored_opm : float

        tolerance : float
            Maximum allowed percentage difference.

        Returns
        -------
        dict
        """

        calculated = FinancialRatios.operating_profit_margin(
            operating_profit=operating_profit,
            sales=sales
        )

        if calculated is None:
            return {
                "status": "SKIPPED",
                "reason": "Invalid input",
                "calculated_opm": None,
                "stored_opm": stored_opm,
                "difference": None
            }

        difference = round(
            abs(calculated - stored_opm),
            2
        )

        return {
            "status": (
                "PASS"
                if difference <= tolerance
                else "FAIL"
            ),
            "calculated_opm": calculated,
            "stored_opm": stored_opm,
            "difference": difference
        }

    @staticmethod
    def validate_roe(
        net_profit,
        equity_capital,
        reserves,
        stored_roe,
        tolerance=1.0
    ):
        """
        Validate Return on Equity.
        """

        calculated = FinancialRatios.return_on_equity(
            net_profit,
            equity_capital,
            reserves
        )

        if calculated is None:

            return {
                "status": "SKIPPED",
                "reason": "Invalid input",
                "calculated_roe": None,
                "stored_roe": stored_roe,
                "difference": None
            }

        difference = round(
            abs(calculated - stored_roe),
            2
        )

        return {
            "status": (
                "PASS"
                if difference <= tolerance
                else "FAIL"
            ),
            "calculated_roe": calculated,
            "stored_roe": stored_roe,
            "difference": difference
        }

    @staticmethod
    def validate_roce(
        ebit,
        equity_capital,
        reserves,
        borrowings,
        stored_roce,
        broad_sector,
        sector_benchmark=12,
        tolerance=1.0
    ):
        """
        Validate Return on Capital Employed.
        """

        calculated = FinancialRatios.return_on_capital_employed(
            ebit,
            equity_capital,
            reserves,
            borrowings
        )

        if calculated is None:

            return {
                "status": "SKIPPED",
                "reason": "Invalid input",
                "calculated_roce": None,
                "stored_roce": stored_roce,
                "difference": None,
                "benchmark_type": None
            }

        difference = round(
            abs(calculated - stored_roce),
            2
        )

        if broad_sector == "Financials":

            benchmark = sector_benchmark
            benchmark_type = "Sector Relative"

        else:

            benchmark = 15
            benchmark_type = "Absolute"

        return {
            "status": (
                "PASS"
                if difference <= tolerance
                else "FAIL"
            ),
            "calculated_roce": calculated,
            "stored_roce": stored_roce,
            "difference": difference,
            "benchmark": benchmark,
            "benchmark_type": benchmark_type
        }

    @staticmethod
    def validate_roa(
        net_profit,
        total_assets,
        stored_roa,
        tolerance=1.0
    ):
        """
        Validate Return on Assets.
        """

        calculated = FinancialRatios.return_on_assets(
            net_profit,
            total_assets
        )

        if calculated is None:

            return {
                "status": "SKIPPED",
                "reason": "Invalid input",
                "calculated_roa": None,
                "stored_roa": stored_roa,
                "difference": None
            }

        difference = round(
            abs(calculated - stored_roa),
            2
        )

        return {
            "status": (
                "PASS"
                if difference <= tolerance
                else "FAIL"
            ),
            "calculated_roa": calculated,
            "stored_roa": stored_roa,
            "difference": difference
        }