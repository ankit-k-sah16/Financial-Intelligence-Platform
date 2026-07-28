"""
Cash Flow Intelligence Engine
N100 Financial Intelligence Platform

Generates:

1. cashflow_intelligence.xlsx
2. distress_alerts.csv


"""

from pathlib import Path
import logging
import numpy as np
import pandas as pd
from math import pow

logger = logging.getLogger(__name__)    

class CashFlowIntelligence:

    def __init__(
        self,
        
        companies_df,
        cashflow_df,
        profitloss_df,
        balancesheet_df,
        sectors_df,
        output_dir,
    ):

        self.companies = companies_df.copy()
        self.cash = cashflow_df.copy()
        self.pnl = profitloss_df.copy()
        self.balance = balancesheet_df.copy()
        self.sectors = sectors_df.copy()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def calculate_cagr(start_value, end_value, years):
        """
        Safely calculate CAGR.

        Returns percentage.
        """

        try:

            if (
                pd.isna(start_value)
                or pd.isna(end_value)
                or years <= 0
                or start_value <= 0
                or end_value <= 0
            ):
                return np.nan

            return round(
                (pow(end_value / start_value, 1 / years) - 1) * 100,
                2,
            )

        except Exception:
            return np.nan

    def _compute_cfo_quality(self, cash_df, pnl_df):
        """
        Average CFO/PAT over last 5 years.
        """

        merged = (
            cash_df.merge(
                pnl_df[
                    [
                        "company_id",
                        "year",
                        "net_profit",
                    ]
                ],
                on=["company_id", "year"],
                how="inner",
            )
            .sort_values("year")
            .tail(5)
        )

        if merged.empty:
            return np.nan, "Unknown"

        merged = merged[
            merged["net_profit"].notna()
            & (merged["net_profit"] != 0)
        ]

        if merged.empty:
            return np.nan, "Unknown"

        merged["ratio"] = (
            merged["operating_activity"]
            / merged["net_profit"]
        )

        score = round(merged["ratio"].mean(), 2)

        if score > 1:
            label = "High Quality"

        elif score >= 0.5:
            label = "Moderate"

        else:
            label = "Accrual Risk"

        return score, label

    def _compute_capex_intensity(
        self,
        cash_df,
        pnl_df,
    ):
        """
        CapEx Intensity =
        ABS(Investing Activity) / Sales ×100
        """

        merged = (
            cash_df.merge(
                pnl_df[
                    [
                        "company_id",
                        "year",
                        "sales",
                    ]
                ],
                on=["company_id", "year"],
                how="inner",
            )
            .sort_values("year")
        )

        if merged.empty:
            return np.nan, "Unknown"

        latest = merged.iloc[-1]

        sales = latest["sales"]

        if pd.isna(sales) or sales == 0:
            return np.nan, "Unknown"

        intensity = round(
            abs(latest["investing_activity"])
            / sales
            * 100,
            2,
        )

        if intensity < 3:
            label = "Asset Light"

        elif intensity <= 8:
            label = "Moderate"

        else:
            label = "Capital Intensive"

        return intensity, label

    def _detect_distress(self, cash_df):
        """
        CFO < 0
        AND
        CFF > 0
        """

        if cash_df.empty:
            return False

        latest = cash_df.sort_values("year").iloc[-1]

        return bool(
            latest["operating_activity"] < 0
            and latest["financing_activity"] > 0
        )

    def _detect_deleveraging(
        self,
        cash_df,
        balance_df,
    ):
        """
        CFF < 0
        AND
        Borrowings declining.
        """

        if (
            len(cash_df) < 2
            or len(balance_df) < 2
        ):
            return False

        latest_cash = (
            cash_df.sort_values("year")
            .iloc[-1]
        )

        balance_df = balance_df.sort_values("year")

        latest = balance_df.iloc[-1]

        previous = balance_df.iloc[-2]

        return bool(
            latest_cash["financing_activity"] < 0
            and latest["borrowings"]
            < previous["borrowings"]
        )

    def _compute_fcf_cagr(
    self,
    cash_df,
):
        """
        CAGR of Free Cash Flow.
        """

        cash_df = (
            cash_df.sort_values("year")
            .tail(5)
            .copy()
        )

        if len(cash_df) < 5:
            return np.nan

        cash_df["fcf"] = (
            cash_df["operating_activity"]
            + cash_df["investing_activity"]
        )

        start = cash_df.iloc[0]["fcf"]

        end = cash_df.iloc[-1]["fcf"]

        return self.calculate_cagr(
            start,
            end,
            4,
        )

    def _compute_fcf_conversion(
    self,
    cash_df,
        pnl_df,
    ):
        """
        FCF / Operating Profit ×100
        """

        merged = (
            cash_df.merge(
                pnl_df[
                    [
                        "company_id",
                        "year",
                        "operating_profit",
                    ]
                ],
                on=["company_id", "year"],
                how="inner",
            )
            .sort_values("year")
        )

        if merged.empty:
            return np.nan

        latest = merged.iloc[-1]

        operating_profit = latest["operating_profit"]

        if (
            pd.isna(operating_profit)
            or operating_profit == 0
        ):
            return np.nan

        fcf = (
            latest["operating_activity"]
            + latest["investing_activity"]
        )

        return round(
            fcf
            / operating_profit
            * 100,
            2,
        )

    def _capital_allocation_label(
        self,
        distress_flag,
        deleveraging_flag,
        capex_label,
    ):
        """
        Final capital allocation interpretation.
        """

        if distress_flag:
            return "Financial Stress"

        if deleveraging_flag:
            return "Debt Reduction"

        if capex_label == "Capital Intensive":
            return "Expansion"

        if capex_label == "Asset Light":
            return "Efficient"

        return "Balanced"

    def _generate_outputs(self):
        """
        Generate Cash Flow Intelligence for all companies.

        Returns
        -------
        pd.DataFrame
            Cash flow intelligence summary.
        """
        self.companies.rename(
            columns={"id": "company_id"},
            inplace=True,
)
        logger.info("Generating Cash Flow Intelligence...")

        output = []
        distress_output = []
          
        
        for _, company in self.companies.iterrows():

            company_id = company["company_id"]
            company_name = company["company_name"]
            sector_row = self.sectors[self.sectors["company_id"] == company_id]
            if sector_row.empty:
                sector = "Unknown"
                           
            else:
                sector = sector_row.iloc[0]["broad_sector"]

            logger.info(f"Processing {company_name}")

            cash = (
                self.cash[
                    self.cash["company_id"] == company_id
                ]
                .sort_values("year")
                .copy()
            )

            pnl = (
                self.pnl[
                    self.pnl["company_id"] == company_id
                ]
                .sort_values("year")
                .copy()
            )

            balance = (
                self.balance[
                    self.balance["company_id"] == company_id
                ]
                .sort_values("year")
                .copy()
            )

    

            if (
                cash.empty
                or pnl.empty
                or balance.empty
            ):
                continue

            try:

                # ----------------------------------
                # CFO Quality
                # ----------------------------------

                cfo_score, cfo_label = (
                    self._compute_cfo_quality(
                        cash,
                        pnl,
                    )
                )

                # ----------------------------------
                # CapEx Intensity
                # ----------------------------------

                capex_pct, capex_label = (
                    self._compute_capex_intensity(
                        cash,
                        pnl,
                    )
                )

                # ----------------------------------
                # FCF CAGR
                # ----------------------------------

                fcf_cagr = self._compute_fcf_cagr(
                    cash,
                )

                # ----------------------------------
                # FCF Conversion
                # ----------------------------------

                fcf_conversion = (
                    self._compute_fcf_conversion(
                        cash,
                        pnl,
                    )
                )

                # ----------------------------------
                # Distress
                # ----------------------------------

                distress_flag = (
                    self._detect_distress(
                        cash,
                    )
                )

                # ----------------------------------
                # Deleveraging
                # ----------------------------------

                deleveraging_flag = (
                    self._detect_deleveraging(
                        cash,
                        balance,
                    )
                )

                # ----------------------------------
                # Capital Allocation
                # ----------------------------------

                allocation = (
                    self._capital_allocation_label(
                        distress_flag,
                        deleveraging_flag,
                        capex_label,
                    )
                )

                # ----------------------------------
                # Main Output
                # ----------------------------------

                output.append({
                    "company_id": company_id,
                    "company_name": company_name,
                    "sector": sector,
                    "cfo_quality_score": cfo_score,
                    "cfo_quality_label": cfo_label,
                    "capex_intensity_pct": capex_pct,
                    "capex_label": capex_label,
                    "fcf_cagr_5yr": fcf_cagr,
                    "fcf_conversion_pct": fcf_conversion,
                    "distress_flag": distress_flag,
                    "deleveraging_flag": deleveraging_flag,
                    "capital_allocation_label": allocation,
                })

                

                # ----------------------------------
                # Distress Alerts
                # ----------------------------------

                if distress_flag:

                    latest_cash = (
                        cash.sort_values("year")
                        .iloc[-1]
                    )

                    latest_pnl = (
                        pnl.sort_values("year")
                        .iloc[-1]
                    )

                    distress_output.append(

                        {
                            "company_id": company_id,
                            "company_name": company_name,
                            "sector": sector,
                            "cfo": latest_cash[
                                "operating_activity"
                            ],
                            "cff": latest_cash[
                                "financing_activity"
                            ],
                            "latest_net_profit": latest_pnl[
                                "net_profit"
                            ],
                        }

                    )

            except Exception as e:

                logger.exception(
                    f"{company_name}: {e}"
                )

        intelligence = pd.DataFrame(output)

        distress = pd.DataFrame(distress_output)

        # --------------------------------------
        # Save Outputs
        # --------------------------------------

        intelligence.to_excel(
            self.output_dir / "cashflow_intelligence.xlsx",
            index=False,
        )

        distress.to_csv(
            self.output_dir / "distress_alerts.csv",
            index=False,
        )

        logger.info(
            f"Generated intelligence for {len(intelligence)} companies."
        )

        logger.info(
            f"Distress alerts: {len(distress)} companies."
        )

        return intelligence
            