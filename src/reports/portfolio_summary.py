"""
Portfolio Summary Report
N100 Financial Intelligence Platform
"""

from pathlib import Path

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
class PortfolioSummary:

    def __init__(self,companies_df,sectors_df,ratios_df,output_dir):

        self.companies = companies_df.copy()

        self.companies.columns = (
            self.companies.columns
            .str.strip()
            .str.lower()
        )

        if "company_id" not in self.companies.columns:
            self.companies.rename(
                columns={"id": "company_id"},
                inplace=True,
            )

        self.sectors = sectors_df.copy()
        self.sectors.columns = (
            self.sectors.columns
            .str.strip()
            .str.lower()
        )

        self.ratios = ratios_df.copy()
        self.ratios.columns = (
            self.ratios.columns
            .str.strip()
            .str.lower()
        )
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
                parents=True,
                exist_ok=True,
            )
        styles = getSampleStyleSheet()

        self.title = styles["Heading1"]
        self.title.alignment = TA_CENTER
        self.heading = styles["Heading2"]
        self.body = styles["BodyText"]

    # -------------------------------------------------------
    def company_page(self, company_id):
        company = self.companies[ self.companies.company_id == company_id ]

        if company.empty:
            return []

        company = company.iloc[0]
        sector = self.sectors[self.sectors.company_id == company_id]
            
        sector = ( "-" if sector.empty 
            else sector.iloc[0]["broad_sector"])
  
        ratio = self.ratios[self.ratios.company_id == company_id ]

        if ratio.empty:
            return []

        ratio = ( ratio.sort_values("year") .iloc[-1])

        def arrow(value, inverse=False):
            if pd.isna(value):
                return "-"

            if inverse:
                return "✓" if value <= 1 else "⚠"

            return "▲" if value >= 0 else "▼"

        story = []

        story.append(
            Paragraph( "N100 Portfolio Summary",self.title,
            )
        )
 
        story.append(Spacer(1, 15)  )
        story.append(
            Paragraph(f"<b>{company.company_name}</b>", self.heading
            )
        )
               
        story.append(
            Paragraph( f"Ticker : <b>{company.company_id}</b>", self.body,   
            )  
        )

        story.append(
            Paragraph(f"Sector : <b>{sector}</b>",self.body,
            ),           
        )
      
        story.append(Spacer(1, 15))
        
        rows = [["Metric", "Value"],
            [
                "ROE",
                f"{arrow(ratio.return_on_equity_pct)} "
                f"{ratio.return_on_equity_pct:.2f}%"
                if pd.notna(ratio.return_on_equity_pct)
                else "-",
            ],

            [
                "Net Margin",
                f"{arrow(ratio.net_profit_margin_pct)} "
                f"{ratio.net_profit_margin_pct:.2f}%"
                if pd.notna(ratio.net_profit_margin_pct)
                else "-",
            ],

            [
                "Operating Margin",
                f"{arrow(ratio.operating_profit_margin_pct)} "
                f"{ratio.operating_profit_margin_pct:.2f}%"
                if pd.notna(ratio.operating_profit_margin_pct)
                else "-",
            ],

            [
                "Debt / Equity",
                f"{arrow(ratio.debt_to_equity,True)} "
                f"{ratio.debt_to_equity:.2f}"
                if pd.notna(ratio.debt_to_equity)
                else "-",
            ],

            [
                "EPS",
                f"{ratio.earnings_per_share:.2f}"
                if pd.notna(ratio.earnings_per_share)
                else "-",
            ],

            [
                "Book Value",
                f"{ratio.book_value_per_share:.2f}"
                if pd.notna(ratio.book_value_per_share)
                else "-",
            ],

            [
                "Free Cash Flow",
                f"{ratio.free_cash_flow_cr:.2f} Cr"
                if pd.notna(ratio.free_cash_flow_cr)
                else "-",
            ],
        ]

        table = Table( rows, colWidths=[180,170] )
    
        table.setStyle(
            TableStyle(
                [
                    ("GRID",(0,0),(-1,-1),0.4,colors.grey),

                    ("BACKGROUND",(0,0),(-1,0),colors.lightgrey),

                    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

                    ("ALIGN",(1,1),(-1,-1),"CENTER"),

                    ("BOTTOMPADDING",(0,0),(-1,-1),6),
                ] )
        )

        story.append(table)
        story.append( Spacer(1,18))

        snapshot = []

        if (pd.notna(ratio.return_on_equity_pct) and ratio.return_on_equity_pct >= 20 ):
 
            snapshot.append("• Excellent ROE")

        elif pd.notna(ratio.return_on_equity_pct):
            snapshot.append("• Moderate shareholder returns")

        if (pd.notna(ratio.debt_to_equity)
            and ratio.debt_to_equity <= 0.5 ):
    
            snapshot.append("• Low debt company")

        elif pd.notna(ratio.debt_to_equity):
            snapshot.append("• Higher leverage")

        if (pd.notna(ratio.free_cash_flow_cr)and ratio.free_cash_flow_cr > 0):
        
            snapshot.append("• Positive free cash flow")

        else:
            snapshot.append("• Weak cash generation")

        if (pd.notna(ratio.net_profit_margin_pct) and ratio.net_profit_margin_pct >= 10):
            snapshot.append("• Healthy profitability")

        story.append( Paragraph("<b>Investment Snapshot</b>",
                self.heading,
            )
        )
        story.append(Spacer(1,8))
    
        for item in snapshot:
            story.append(Paragraph(item,self.body 
                )        
            )

        story.append( Spacer(1,15))

        info = [ ["Website", company.website or "-"],
            ["Face Value",
             str(company.face_value)
             if pd.notna(company.face_value)
             else "-"],

            ["Book Value",
             str(company.book_value)
             if pd.notna(company.book_value)
             else "-"],
        ]
        info_table = Table(info,colWidths=[110,240],)

        info_table.setStyle(
            TableStyle(
                [   ("GRID",(0,0),(-1,-1),0.4,colors.grey),
                    ("BACKGROUND",(0,0),(0,-1),colors.whitesmoke),
                    ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
                    ("BOTTOMPADDING",(0,0),(-1,-1),6),
                ]
            ))

        story.append(info_table)

        story.append(Spacer(1,18))

        story.append(
            Paragraph(
                "<font size=8 color='grey'>"
                "Generated by N100 Financial Intelligence Platform"
                "</font>",

                self.body,
            )
        )

        return story
    
    # -------------------------------------------------------
    def build(self, output_path):

        story = []
        companies = (self.companies
            .sort_values("company_id")
        )

        for _, row in companies.iterrows():
            page = self.company_page(row["company_id"])

            if not page:
                continue

            story.extend(page)
            story.append(PageBreak())

        if story and isinstance(story[-1], PageBreak):
            story.pop()

        doc = SimpleDocTemplate(str(output_path))

        doc.build(story)