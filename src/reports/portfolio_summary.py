"""
Portfolio Summary Report
N100 Financial Intelligence Platform

Generates one-page summary per company.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.lib.enums import TA_CENTER


class PortfolioSummary:

    def __init__(self, data_provider):

        self.data = data_provider

        self.styles = getSampleStyleSheet()

        self.styles["Heading1"].alignment = TA_CENTER

    # ---------------------------------------------------------
    # Trend Arrow
    # ---------------------------------------------------------

    @staticmethod
    def trend_arrow(current, previous, higher_is_better=True):

        if pd.isna(current) or pd.isna(previous):
            return "—"

        if previous == 0:
            return "—"

        change = (current - previous) / abs(previous)

        if abs(change) <= 0.02:
            return "→"

        if higher_is_better:

            return "↑" if change > 0 else "↓"

        return "↑" if change < 0 else "↓"

    # ---------------------------------------------------------
    # Format Value
    # ---------------------------------------------------------

    @staticmethod
    def fmt(value, suffix=""):

        try:

            if pd.isna(value):
                return "-"

            return f"{float(value):,.2f}{suffix}"

        except Exception:

            return "-"

    # ---------------------------------------------------------
    # Latest + Previous Row
    # ---------------------------------------------------------

    def latest_rows(self, df):

        if df.empty:
            return None, None

        df = df.copy()

        df["year_dt"] = pd.to_datetime(
            df["year"],
            format="mixed",
            errors="coerce",
        )

        df = (
            df.dropna(subset=["year_dt"])
            .sort_values("year_dt")
            .tail(2)
        )

        if len(df) == 1:
            return df.iloc[-1], None

        return df.iloc[-1], df.iloc[-2]

    # ---------------------------------------------------------
    # Build Company Page
    # ---------------------------------------------------------

    def company_page(self, company_id):

        story = []

        company = self.data._company_info(company_id)

        pnl = self.data._profitloss(company_id)

        balance = self.data._balancesheet(company_id)

        latest_pnl, prev_pnl = self.latest_rows(pnl)

        latest_bs, prev_bs = self.latest_rows(balance)

        story.append(
            Paragraph(
                f"<b>{company['company_name']}</b>",
                self.styles["Heading1"],
            )
        )

        story.append(
            Paragraph(
                f"{company['company_id']} | {company['sector']}",
                self.styles["Heading2"],
            )
        )

        story.append(Spacer(1, 12))

        def value(df, col):

            if df is None:
                return np.nan

            return df.get(col, np.nan)

        revenue = value(latest_pnl, "sales")
        revenue_prev = value(prev_pnl, "sales")

        profit = value(latest_pnl, "net_profit")
        profit_prev = value(prev_pnl, "net_profit")

        eps = value(latest_pnl, "eps")
        eps_prev = value(prev_pnl, "eps")

        roe = value(latest_pnl, "roe")
        roe_prev = value(prev_pnl, "roe")

        roce = value(latest_pnl, "roce")
        roce_prev = value(prev_pnl, "roce")

        de = value(latest_bs, "debt_to_equity")
        de_prev = value(prev_bs, "debt_to_equity")

        rows = [

            [
                "Revenue",
                self.fmt(revenue),
                self.trend_arrow(revenue, revenue_prev),
            ],

            [
                "Net Profit",
                self.fmt(profit),
                self.trend_arrow(profit, profit_prev),
            ],

            [
                "EPS",
                self.fmt(eps),
                self.trend_arrow(eps, eps_prev),
            ],

            [
                "ROE",
                self.fmt(roe, "%"),
                self.trend_arrow(roe, roe_prev),
            ],

            [
                "ROCE",
                self.fmt(roce, "%"),
                self.trend_arrow(roce, roce_prev),
            ],

            [
                "Debt / Equity",
                self.fmt(de),
                self.trend_arrow(
                    de,
                    de_prev,
                    higher_is_better=False,
                ),
            ],

        ]

        table = Table(
            rows,
            colWidths=[170, 150, 60],
        )

        table.setStyle(

            TableStyle(

                [

                    ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),

                    ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),

                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),

                    ("ALIGN", (1, 0), (-1, -1), "CENTER"),

                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),

                    ("TOPPADDING", (0, 0), (-1, -1), 6),

                ]

            )

        )

        story.append(table)

        story.append(Spacer(1, 20))

        story.append(

            Paragraph(

                "<font size=9>Generated by N100 Financial Intelligence Platform</font>",

                self.styles["Normal"],

            )

        )

        return story

    # ---------------------------------------------------------
    # Generate Portfolio Summary
    # ---------------------------------------------------------

    def build(self, output_path):

        doc = SimpleDocTemplate(str(output_path))

        story = []

        companies = self.data.companies_df.copy()
        print(companies.columns.tolist())
        companies = companies.sort_values("company_id").reset_index(drop=True)

        for _, row in companies.iterrows():

            company_story = self.company_page(
                row["company_id"]
            )

            story.extend(company_story)

            from reportlab.platypus import PageBreak

            story.append(PageBreak())

        doc.build(story)

        return Path(output_path)