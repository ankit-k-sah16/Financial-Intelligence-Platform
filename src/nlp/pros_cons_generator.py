"""
Pros & Cons Generator
---------------------

Generates investment pros and cons based on
financial quality, profitability, leverage,
cash flow and growth signals.

"""

from __future__ import annotations
import logging
from pathlib import Path
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

class ProsConsGenerator:
    """
    Generates investment pros and cons using
    rule-based financial analytics.
    """

    def __init__(self, confidence_threshold: int = 60):
        self.confidence_threshold = confidence_threshold

    # ---------------------------------------------------------
    # Confidence Score
    # ---------------------------------------------------------
    @staticmethod
    def confidence(score: float) -> int:
        """
        Converts a raw rule score into a
        confidence percentage (0-100).
        """
        return int(max(0, min(100, round(score))))

    # ---------------------------------------------------------
    # Consecutive Positive Values
    # ---------------------------------------------------------

    @staticmethod
    def consecutive_positive(series: pd.Series) -> int:
        """
        Counts consecutive positive values
        starting from the latest year.
        """

        count = 0

        for value in reversed(series.fillna(0).tolist()):

            if value > 0:
                count += 1
            else:
                break

        return count

    # ---------------------------------------------------------
    # Consecutive Negative Values
    # ---------------------------------------------------------

    @staticmethod
    def consecutive_negative(series: pd.Series) -> int:
        """
        Counts consecutive negative values
        starting from the latest year.
        """

        count = 0

        for value in reversed(series.fillna(0).tolist()):

            if value < 0:
                count += 1
            else:
                break

        return count

    # ---------------------------------------------------------
    # Consecutive Increasing
    # ---------------------------------------------------------

    @staticmethod
    def consecutive_increasing(series: pd.Series) -> int:
        """
        Counts consecutive years of increase.
        """

        values = series.dropna().tolist()

        if len(values) < 2:
            return 0

        count = 0

        for i in range(len(values) - 1, 0, -1):

            if values[i] > values[i - 1]:
                count += 1
            else:
                break

        return count

    # ---------------------------------------------------------
    # Consecutive Decreasing
    # ---------------------------------------------------------

    @staticmethod
    def consecutive_decreasing(series: pd.Series) -> int:
        """
        Counts consecutive years of decline.
        """

        values = series.dropna().tolist()

        if len(values) < 2:
            return 0

        count = 0

        for i in range(len(values) - 1, 0, -1):

            if values[i] < values[i - 1]:
                count += 1
            else:
                break

        return count

    # ---------------------------------------------------------
    # CAGR
    # ---------------------------------------------------------

    @staticmethod
    def calculate_cagr(start_value, end_value, years):
        """
        Calculates CAGR safely.
        """

        try:
            if (
                start_value is None
                or end_value is None
                or years <= 0
                or start_value <= 0
            ):
                return np.nan

            return (
                ((end_value / start_value) ** (1 / years) - 1)
                * 100
            )

        except Exception:
            return np.nan

    # ---------------------------------------------------------
    # Safe Latest Value
    # ---------------------------------------------------------

    @staticmethod
    def latest(series: pd.Series):

        if series.empty:
            return np.nan

        return series.iloc[-1]

    # ---------------------------------------------------------
    # Adding Rule
    # ---------------------------------------------------------

    def add_rule(self, output,company_id,rule_type,rule_id, text,confidence, ):

        """
        Adds rule to output if confidence
        exceeds threshold.
        """

        confidence = self.confidence(confidence)

        if confidence < self.confidence_threshold:
            return

        output.append(
            {   "company_id": company_id,
                "type": rule_type,
                "rule_id": rule_id,
                "text": text,
                "confidence_pct": confidence,
            }
        )

        # ---------------------------------------------------------
    # PRO RULE 1
    # ROE > 20% sustained for 3+ years
    # ---------------------------------------------------------

    def pro_rule_1(self, company_id, df, output):

        recent = (
            df.sort_values("year")
              .tail(3)
        )

        if len(recent) < 3:
            return

        if (recent["return_on_equity_pct"] > 20).all():

            confidence = min(
                100,
                80 + (
                    recent["return_on_equity_pct"].mean() - 20
                )
            )

            self.add_rule(
                output,
                company_id,
                "pro",
                "PRO_01",
                (
                    "Consistently high return on equity above 20% "
                    "demonstrates exceptional capital efficiency."
                ),
                confidence,
            )

    # ---------------------------------------------------------
    # PRO RULE 2
    # Positive FCF for 5 consecutive years
    # ---------------------------------------------------------

    def pro_rule_2(self, company_id, df, output):

        recent = (
            df.sort_values("year")
              .tail(5)
        )

        if len(recent) < 5:
            return

        if self.consecutive_positive(
            recent["free_cash_flow_cr"]
        ) >= 5:

            confidence = min(
                100,
                85 + recent["free_cash_flow_cr"].mean() / 500
            )

            self.add_rule(
                output,
                company_id,
                "pro",
                "PRO_02",
                (
                    "Strong free cash flow generation over 5 years "
                    "signals healthy business fundamentals."
                ),
                confidence,
            )

    # ---------------------------------------------------------
    # PRO RULE 3
    # Debt Free
    # ---------------------------------------------------------

    def pro_rule_3(self, company_id, df, output):

        latest = df.sort_values("year").iloc[-1]

        if latest["debt_to_equity"] == 0:

            self.add_rule(
                output,
                company_id,
                "pro",
                "PRO_03",
                (
                    "Debt-free balance sheet provides financial "
                    "flexibility and eliminates interest burden."
                ),
                95,
            )

    # ---------------------------------------------------------
    # PRO RULE 4
    # Revenue CAGR > 15%
    # ---------------------------------------------------------

    def pro_rule_4(self, company_id, pnl_df, output):

        pnl_df = pnl_df.sort_values("year")

        if len(pnl_df) < 5:
            return

        recent = pnl_df.sort_values("year").tail(5)

        if len(recent) < 5:
            return

        start = recent.iloc[0]["sales"]
        end = recent.iloc[-1]["sales"]

        earliest_year = pd.to_numeric(
            recent.iloc[0]["year"],
            errors="coerce")


        latest_year = pd.to_numeric(
            recent.iloc[-1]["year"],
            errors="coerce"
        )

        if pd.isna(earliest_year) or pd.isna(latest_year):
            return

        years = int(latest_year - earliest_year)

        if years <= 0:
            return

        cagr = self.calculate_cagr(
            start,
            end,
            years,
        )

        if pd.notna(cagr) and cagr > 15:

            confidence = min(
                100,
                75 + (cagr - 15)
            )

            self.add_rule(
                output,
                company_id,
                "pro",
                "PRO_04",
                (
                    "Revenue growing at above 15% CAGR over 5 years "
                    "reflects strong business momentum."
                ),
                confidence,
            )

    # ---------------------------------------------------------
    # PRO RULE 5
    # Operating Margin >25%
    # ---------------------------------------------------------

    def pro_rule_5(self, company_id, df, output):

        latest = df.sort_values("year").iloc[-1]

        opm = latest["operating_profit_margin_pct"]

        if opm > 25:

            confidence = min(
                100,
                80 + (opm - 25)
            )

            self.add_rule(
                output,
                company_id,
                "pro",
                "PRO_05",
                (
                    "Operating profit margin above 25% indicates "
                    "strong pricing power and cost discipline."
                ),
                confidence,
            )

    # ---------------------------------------------------------
    # PRO RULE 6
    # PAT CAGR >20%
    # ---------------------------------------------------------

    def pro_rule_6(self, company_id, pnl_df, output):

        pnl_df = pnl_df.sort_values("year")

        if len(pnl_df) < 5:
            return

        recent = pnl_df.sort_values("year").tail(5)

        if len(recent) < 5:
            return

        start = recent.iloc[0]["net_profit"]
        end = recent.iloc[-1]["net_profit"]

        earliest_year = pd.to_numeric(
            recent.iloc[0]["year"],
            errors="coerce"
)

        latest_year = pd.to_numeric(
            recent.iloc[-1]["year"],
            errors="coerce"
        )

        if pd.isna(earliest_year) or pd.isna(latest_year):
            return

        years = int(latest_year - earliest_year)

        if years <= 0:
            return

        cagr = self.calculate_cagr(
            start,
            end,
            years,
        )

        if pd.notna(cagr) and cagr > 20:

            confidence = min(
                100,
                80 + (cagr - 20)
            )

            self.add_rule(
                output,
                company_id,
                "pro",
                "PRO_06",
                (
                    "Net profit compounding at above 20% over "
                    "5 years creates significant shareholder value."
                ),
                confidence,
            )
        # ---------------------------------------------------------
    # PRO RULE 7
    # Interest Coverage > 10 OR Debt Free
    # ---------------------------------------------------------

    def pro_rule_7(self, company_id, df, output):

        latest = df.sort_values("year").iloc[-1]

        icr = latest["interest_coverage"]
        de = latest["debt_to_equity"]

        if (pd.notna(icr) and icr > 10) or de == 0:

            confidence = 90

            if pd.notna(icr):
                confidence = min(100, 85 + icr / 5)

            self.add_rule(
                output,
                company_id,
                "pro",
                "PRO_07",
                (
                    "Very high interest coverage ratio reflects "
                    "negligible financial stress from debt servicing."
                ),
                confidence,
            )

    # ---------------------------------------------------------
    # PRO RULE 8
    # Dividend Yield >2% with Positive FCF
    # ---------------------------------------------------------

    def pro_rule_8(self, company_id, ratios_df, valuation_df, output):

        latest_ratio = ratios_df.sort_values("year").iloc[-1]
        latest_val = valuation_df.sort_values("year").iloc[-1]

        dividend = latest_val["dividend_yield_pct"]
        fcf = latest_ratio["free_cash_flow_cr"]

        if (
            pd.notna(dividend)
            and dividend > 2
            and pd.notna(fcf)
            and fcf > 0
        ):

            confidence = min(100, 80 + dividend * 3)

            self.add_rule(
                output,
                company_id,
                "pro",
                "PRO_08",
                (
                    "Consistent dividend yield above 2% backed "
                    "by positive free cash flow."
                ),
                confidence,
            )

    # ---------------------------------------------------------
    # PRO RULE 9
    # EPS CAGR >15%
    # ---------------------------------------------------------

    def pro_rule_9(self, company_id, df, output):

        df = df.sort_values("year")

        if len(df) < 5:
            return

        recent = df.sort_values("year").tail(5)

        if len(recent) < 5:
            return

        start = recent.iloc[0]["earnings_per_share"]
        end = recent.iloc[-1]["earnings_per_share"]

        earliest_year = pd.to_numeric(
            recent.iloc[0]["year"],
            errors="coerce"
    )

        latest_year = pd.to_numeric(
            recent.iloc[-1]["year"],
            errors="coerce"
        )

        if pd.isna(earliest_year) or pd.isna(latest_year):
            return

        years = int(latest_year - earliest_year)

        if years <= 0:
            return

        cagr = self.calculate_cagr(
            start,
            end,
            years,
        )

        if pd.notna(cagr) and cagr > 15:

            confidence = min(100, 80 + (cagr - 15))

            self.add_rule(
                output,
                company_id,
                "pro",
                "PRO_09",
                (
                    "Earnings per share growing above 15% CAGR "
                    "indicates strong earnings quality and compounding."
                ),
                confidence,
            )

    # ---------------------------------------------------------
    # PRO RULE 10
    # ROE Improving for 3 Years
    # ---------------------------------------------------------

    def pro_rule_10(self, company_id, df, output):

        recent = (
            df.sort_values("year")
              .tail(3)
        )

        if len(recent) < 3:
            return

        if self.consecutive_increasing(
            recent["return_on_equity_pct"]
        ) >= 2:

            confidence = 85

            self.add_rule(
                output,
                company_id,
                "pro",
                "PRO_10",
                (
                    "Return on equity improving for 3 consecutive "
                    "years shows strengthening business quality."
                ),
                confidence,
            )

    # ---------------------------------------------------------
    # PRO RULE 11
    # Revenue CAGR > PAT CAGR (Operating Leverage)
    # ---------------------------------------------------------

    def pro_rule_11(self, company_id, pnl_df, output):

        pnl_df = pnl_df.sort_values("year")

        if len(pnl_df) < 5:
            return

        revenue_cagr = self.calculate_cagr(
            pnl_df.iloc[-5]["sales"],
            pnl_df.iloc[-1]["sales"],
            5,
        )

        pat_cagr = self.calculate_cagr(
            pnl_df.iloc[-5]["net_profit"],
            pnl_df.iloc[-1]["net_profit"],
            5,
        )

        # Rule text indicates profits are growing faster than revenue
        if (
            pd.notna(revenue_cagr)
            and pd.notna(pat_cagr)
            and pat_cagr > revenue_cagr
        ):

            confidence = min(
                100,
                80 + (pat_cagr - revenue_cagr)
            )

            self.add_rule(
                output,
                company_id,
                "pro",
                "PRO_11",
                (
                    "Revenue growing slower than profits shows "
                    "improving operating leverage and scale benefits."
                ),
                confidence,
            )

    # ---------------------------------------------------------
    # PRO RULE 12
    # Assets Increasing with Declining Debt
    # ---------------------------------------------------------

    def pro_rule_12(
        self,
        company_id,
        balance_df,
        ratios_df,
        output,
    ):

        balance_df = balance_df.sort_values("year")
        ratios_df = ratios_df.sort_values("year")

        if len(balance_df) < 3 or len(ratios_df) < 3:
            return

        assets_up = (
            self.consecutive_increasing(
                balance_df["total_assets"]
            ) >= 2
        )

        debt_down = (
            self.consecutive_decreasing(
                ratios_df["total_debt_cr"]
            ) >= 2
        )

        if assets_up and debt_down:

            self.add_rule(
                output,
                company_id,
                "pro",
                "PRO_12",
                (
                    "Growing asset base funded by internal "
                    "accruals reflects self-sustaining growth."
                ),
                90,
            )

        # ---------------------------------------------------------
    # CON RULE 1
    # Debt to Equity > 2
    # ---------------------------------------------------------

    def con_rule_1(self, company_id, ratios_df, output):

        latest = ratios_df.sort_values("year").iloc[-1]

        de = latest["debt_to_equity"]

        if pd.notna(de) and de > 2:

            confidence = min(100, 70 + de * 8)

            self.add_rule(
                output,
                company_id,
                "con",
                "CON_01",
                (
                    f"Debt-to-equity ratio of {de:.2f} is elevated "
                    "for a non-financial company and warrants monitoring."
                ),
                confidence,
            )

    # ---------------------------------------------------------
    # CON RULE 2
    # Negative FCF for 3 Consecutive Years
    # ---------------------------------------------------------

    def con_rule_2(self, company_id, ratios_df, output):

        recent = (
            ratios_df.sort_values("year")
            .tail(3)
        )

        if len(recent) < 3:
            return

        if self.consecutive_negative(
            recent["free_cash_flow_cr"]
        ) >= 3:

            self.add_rule(
                output,
                company_id,
                "con",
                "CON_02",
                (
                    "Free cash flow negative for 3 consecutive years "
                    "raises concern about cash generation quality."
                ),
                90,
            )

    # ---------------------------------------------------------
    # CON RULE 3
    # OPM Declining 3 Years
    # ---------------------------------------------------------

    def con_rule_3(self, company_id, ratios_df, output):

        recent = (
            ratios_df.sort_values("year")
            .tail(3)
        )

        if len(recent) < 3:
            return

        if self.consecutive_decreasing(
            recent["operating_profit_margin_pct"]
        ) >= 2:

            self.add_rule(
                output,
                company_id,
                "con",
                "CON_03",
                (
                    "Operating margins declining for 3 consecutive "
                    "years suggest pricing or cost pressure."
                ),
                85,
            )

    # ---------------------------------------------------------
    # CON RULE 4
    # Latest Net Profit Negative
    # ---------------------------------------------------------

    def con_rule_4(self, company_id, profitloss_df, output):

        latest = (
            profitloss_df.sort_values("year")
            .iloc[-1]
        )

        if latest["net_profit"] < 0:

            self.add_rule(
                output,
                company_id,
                "con",
                "CON_04",
                (
                    "Company reported a net loss in the most "
                    "recent financial year."
                ),
                95,
            )

    # ---------------------------------------------------------
    # CON RULE 5
    # Revenue Declining for 2 Years
    # ---------------------------------------------------------

    def con_rule_5(self, company_id, profitloss_df, output):

        recent = (
            profitloss_df.sort_values("year")
            .tail(3)
        )

        if len(recent) < 3:
            return

        if self.consecutive_decreasing(
            recent["sales"]
        ) >= 2:

            self.add_rule(
                output,
                company_id,
                "con",
                "CON_05",
                (
                    "Revenue contraction over 2 consecutive years "
                    "indicates demand weakness or market share loss."
                ),
                85,
            )

    # ---------------------------------------------------------
    # CON RULE 6
    # Interest Coverage < 1.5
    # ---------------------------------------------------------

    def con_rule_6(self, company_id, ratios_df, output):

        latest = ratios_df.sort_values("year").iloc[-1]

        icr = latest["interest_coverage"]

        if pd.notna(icr) and icr < 1.5:

            confidence = max(65, 100 - icr * 20)

            self.add_rule(
                output,
                company_id,
                "con",
                "CON_06",
                (
                    "Interest coverage ratio below 1.5x indicates "
                    "the company is at risk of not meeting its debt obligations."
                ),
                confidence,
            )

        # ---------------------------------------------------------
    # CON RULE 7
    # Dividend Payout > 100%
    # ---------------------------------------------------------

    def con_rule_7(self, company_id, profitloss_df, output):

        latest = profitloss_df.sort_values("year").iloc[-1]

        payout = latest["dividend_payout"]

        if pd.notna(payout) and payout > 100:

            confidence = min(100, 75 + (payout - 100) / 2)

            self.add_rule(
                output,
                company_id,
                "con",
                "CON_07",
                (
                    "Dividend payout ratio above 100% means the "
                    "company is paying dividends from reserves, "
                    "which is unsustainable."
                ),
                confidence,
            )

    # ---------------------------------------------------------
    # CON RULE 8
    # Debt-to-Equity Rising for 3 Years
    # ---------------------------------------------------------

    def con_rule_8(self, company_id, ratios_df, output):

        recent = (
            ratios_df
            .sort_values("year")
            .tail(3)
        )

        if len(recent) < 3:
            return

        if self.consecutive_increasing(
            recent["debt_to_equity"]
        ) >= 2:

            self.add_rule(
                output,
                company_id,
                "con",
                "CON_08",
                (
                    "Rising debt-to-equity ratio over 3 years "
                    "suggests increasing financial leverage risk."
                ),
                85,
            )

    # ---------------------------------------------------------
    # CON RULE 9
    # EPS Declining for 3 Years
    # ---------------------------------------------------------

    def con_rule_9(self, company_id, profitloss_df, output):

        recent = (
            profitloss_df
            .sort_values("year")
            .tail(3)
        )

        if len(recent) < 3:
            return

        if self.consecutive_decreasing(
            recent["eps"]
        ) >= 2:

            self.add_rule(
                output,
                company_id,
                "con",
                "CON_09",
                (
                    "Earnings per share declining for 3 consecutive "
                    "years reflects deteriorating profitability."
                ),
                90,
            )

    # ---------------------------------------------------------
    # CON RULE 10
    # ROCE < 10%
    # ---------------------------------------------------------

    def con_rule_10(self, company_id, valuation_df, output):

        if "roce" not in valuation_df.columns:
            return

        latest = valuation_df.sort_values("year").iloc[-1]

        roce = latest["roce"]

        if pd.notna(roce) and roce < 10:

            confidence = max(65, 95 - roce)

            self.add_rule(
                output,
                company_id,
                "con",
                "CON_10",
                (
                    "Return on capital employed below 10% suggests "
                    "the business is not generating sufficient "
                    "returns on invested capital."
                ),
                confidence,
            )

    # ---------------------------------------------------------
    # CON RULE 11
    # Net Debt > 3 × EBITDA
    # ---------------------------------------------------------

    def con_rule_11(
        self,
        company_id,
        balancesheet_df,
        marketcap_df,
        output,
    ):

        latest_bs = (
            balancesheet_df
            .sort_values("year")
            .iloc[-1]
        )

        latest_mc = (
            marketcap_df
            .sort_values("year")
            .iloc[-1]
        )

        if (
            "enterprise_value_crore" not in latest_mc.index
            or "ev_ebitda" not in latest_mc.index
        ):
            return

        if (
            pd.isna(latest_mc["enterprise_value_crore"])
            or pd.isna(latest_mc["ev_ebitda"])
            or latest_mc["ev_ebitda"] == 0
        ):
            return

        ebitda = (
            latest_mc["enterprise_value_crore"]
            / latest_mc["ev_ebitda"]
        )

        net_debt = latest_bs["borrowings"]

        if pd.notna(net_debt) and ebitda > 0:

            leverage = net_debt / ebitda

            if leverage > 3:

                confidence = min(
                    100,
                    75 + leverage * 5
                )

                self.add_rule(
                    output,
                    company_id,
                    "con",
                    "CON_11",
                    (
                        "Net debt exceeding 3 times EBITDA is a "
                        "high leverage ratio and limits financial flexibility."
                    ),
                    confidence,
                )

    # ---------------------------------------------------------
    # CON RULE 12
    # Revenue CAGR < 5%
    # ---------------------------------------------------------

    def con_rule_12(self, company_id, profitloss_df, output):

        profitloss_df = profitloss_df.sort_values("year")

        if len(profitloss_df) < 5:
            return

        recent = profitloss_df.sort_values("year").tail(5)

        if len(recent) < 5:
            return

        start_sales = recent.iloc[0]["sales"]
        end_sales = recent.iloc[-1]["sales"]

        earliest_year = pd.to_numeric(
            recent.iloc[0]["year"],
            errors="coerce"
        )

        latest_year = pd.to_numeric(
            recent.iloc[-1]["year"],
            errors="coerce"
        )

        if pd.isna(earliest_year) or pd.isna(latest_year):
            return

        years = int(latest_year - earliest_year)
        if years <= 0:
            return

        revenue_cagr = self.calculate_cagr(
            start_sales,
            end_sales,
            years,
        )

        if (
            pd.notna(revenue_cagr)
            and revenue_cagr < 5
        ):

            confidence = max(
                65,
                90 - revenue_cagr
            )

            self.add_rule(
                output,
                company_id,
                "con",
                "CON_12",
                (
                    "Revenue growing at below 5% over 5 years "
                    "lags inflation and suggests limited business momentum."
                ),
                confidence,
            )
            
    def generate(self, companies_df,ratios_df,balancesheet_df,profitloss_df, cashflow_df,       
        market_cap_df, valuation_summary_df,valuation_flag_df, ):
   
        """
        Generate Pros & Cons for every company.

        Returns
        -------
        DataFrame
            company_id
            company_name
            type
            rule
            message
            confidence
        """

        output = []

        logger.info("Generating Pros & Cons...")
                                             
                        
        for _, company in companies_df.iterrows():

            company_id = company["company_id"]
            company_name = company["company_name"]

            logger.info(f"Processing {company_name}")

            ratio = (
                ratios_df[ ratios_df["company_id"] == company_id] .sort_values("year").copy())

            pnl = (profitloss_df[profitloss_df["company_id"] == company_id ].sort_values("year").copy())
                 

            balance = ( balancesheet_df[ balancesheet_df["company_id"] == company_id
                ].sort_values("year") .copy())

            cash = (cashflow_df[cashflow_df["company_id"] == company_id ]
                .sort_values("year").copy() )
            
            market = ( market_cap_df[ market_cap_df["company_id"] == company_id]
                .sort_values("year").copy())

            valuation = ( valuation_summary_df[
                    valuation_summary_df["company_id"] == company_id].copy()
            )

            valuation_flag = (valuation_flag_df[
                    valuation_flag_df["company_id"] == company_id ].copy())
                
            if ratio.empty:
                continue

            try:

                # ---------- PRO RULES ----------

                self.pro_rule_1(company_id, ratio, output)

                self.pro_rule_2(company_id, ratio, output)

                self.pro_rule_3(company_id, ratio, output)

                self.pro_rule_4(company_id, pnl, output)

                self.pro_rule_5(company_id, ratio, output)

                self.pro_rule_6(company_id, pnl, output)

                self.pro_rule_7(company_id, ratio, output)

                self.pro_rule_8(company_id,ratio,market, output,)
                
                self.pro_rule_9(company_id, ratio, output)

                self.pro_rule_10(company_id, ratio, output)

                self.pro_rule_11(company_id, pnl, output)

                self.pro_rule_12(company_id, balance,ratio ,output)

                # ---------- CON RULES ----------

                self.con_rule_1(company_id, ratio, output)

                self.con_rule_2(company_id, ratio, output)

                self.con_rule_3(company_id, ratio, output)

                self.con_rule_4(company_id, pnl, output)

                self.con_rule_5(company_id, pnl, output)

                self.con_rule_6(company_id, ratio, output)

                self.con_rule_7(company_id, pnl, output)

                self.con_rule_8(company_id, ratio, output)

                self.con_rule_9(company_id, pnl, output)

                self.con_rule_10(company_id, market, output)

                self.con_rule_11(company_id,  market,valuation,
                    output,
                )

                self.con_rule_12(company_id, pnl, output)

            except Exception as e:

                logger.exception(f"{company_name}: {e}"  )

        result = pd.DataFrame(output)

        if result.empty:
            logger.warning("No Pros & Cons generated.")
            return result

        # -----------------------------
        # Add Company Name
        # -----------------------------
        result = result.merge(

            companies_df[
                [
                    "company_id",
                    "company_name",
                ]
            ], on="company_id", how="left" , )

        # -----------------------------
        # Validation
        # -----------------------------
        validation = ( result .groupby(["company_id","type", ]).size().unstack(fill_value=0))

        for cid, row in validation.iterrows():

            if row.get("PRO", 0) == 0:
                logger.warning(f"{cid} has no PRO generated.")
  
            if row.get("CON", 0) == 0:
                logger.warning( f"{cid} has no CON generated.")
               
        logger.info( f"Generated {len(result)} Pros & Cons.")     

        return result           

        