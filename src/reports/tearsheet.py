"""
Company Tear Sheet Generator
N100 Financial Intelligence Platform

Generates professional 2-page PDF company tear sheets
using ReportLab.

Version: 1.0
"""

from pathlib import Path
import logging
import pandas as pd
import numpy as np

# ---------------------------------------------------------
# ReportLab
# ---------------------------------------------------------

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import (
    TA_CENTER,
    TA_LEFT,
    TA_RIGHT,
)
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.platypus import PageBreak
from reportlab.platypus import (

    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,

)

from reportlab.graphics.shapes import (
    Drawing,String,Rect,Line
    
)

from reportlab.graphics.charts.barcharts import (
    VerticalBarChart,
)

from reportlab.graphics.charts.linecharts import (
    HorizontalLineChart,
)

from reportlab.graphics.charts.legends import (
    Legend,
)

# ---------------------------------------------------------
# Logger
# ---------------------------------------------------------

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Color Palette
# ---------------------------------------------------------

NAVY = HexColor("#0B1F3A")

BLUE = HexColor("#1F77B4")

LIGHT_BLUE = HexColor("#DCEEFF")

GREEN = HexColor("#2E8B57")

LIGHT_GREEN = HexColor("#EAF7EA")

RED = HexColor("#C0392B")

LIGHT_RED = HexColor("#FDEDEC")

ORANGE = HexColor("#F39C12")

GRAY = HexColor("#6E6E6E")

LIGHT_GRAY = HexColor("#F5F5F5")

BORDER = HexColor("#D0D0D0")

WHITE = colors.white

BLACK = colors.black

# ---------------------------------------------------------
# Layout Constants
# ---------------------------------------------------------

PAGE_WIDTH = 11 * inch

PAGE_HEIGHT = 8.5 * inch

LEFT_MARGIN = 0.40 * inch

RIGHT_MARGIN = 0.40 * inch

TOP_MARGIN = 0.40 * inch

BOTTOM_MARGIN = 0.40 * inch

HEADER_HEIGHT = 0.55 * inch

KPI_TILE_WIDTH = 2.90 * inch

KPI_TILE_HEIGHT = 0.85 * inch

CHART_WIDTH = 4.75 * inch

CHART_HEIGHT = 2.35 * inch

SECTION_GAP = 0.18 * inch

# ---------------------------------------------------------
# Paragraph Styles
# ---------------------------------------------------------
styles=getSampleStyleSheet()
TITLE_STYLE = ParagraphStyle(

    "TITLE_STYLE",

    parent=styles["Heading1"],

    alignment=TA_LEFT,

    fontName="Helvetica-Bold",

    fontSize=22,

    leading=26,

    textColor=WHITE,

)

SUBTITLE_STYLE = ParagraphStyle(

    "SUBTITLE_STYLE",

    parent=styles["BodyText"],

    alignment=TA_LEFT,

    fontName="Helvetica",

    fontSize=10,

    textColor=WHITE,

)

SECTION_TITLE_STYLE = ParagraphStyle(

    "SECTION_TITLE_STYLE",

    parent=styles["Heading2"],

    fontName="Helvetica-Bold",

    fontSize=13,

    textColor=NAVY,

    spaceAfter=6,

)

KPI_TITLE_STYLE = ParagraphStyle(

    "KPI_TITLE_STYLE",

    parent=styles["BodyText"],

    alignment=TA_CENTER,

    fontName="Helvetica",

    fontSize=9,

    textColor=GRAY,

)

KPI_VALUE_STYLE = ParagraphStyle(

    "KPI_VALUE_STYLE",

    parent=styles["Heading2"],

    alignment=TA_CENTER,

    fontName="Helvetica-Bold",

    fontSize=15,

    textColor=NAVY,

)
BODY_STYLE = ParagraphStyle(

    "BODY_STYLE",

    parent=styles["BodyText"],

    fontName="Helvetica",

    fontSize=9,

    leading=12,

)

GOOD_STYLE = ParagraphStyle(

    "GOOD_STYLE",

    parent=BODY_STYLE,

    bulletIndent=12,

    leftIndent=18,

    textColor=GREEN,

)

BAD_STYLE = ParagraphStyle(

    "BAD_STYLE",

    parent=BODY_STYLE,

    bulletIndent=12,

    leftIndent=18,

    textColor=RED,

)

# ---------------------------------------------------------
# Tear Sheet Generator
# ---------------------------------------------------------


class CompanyTearSheet:
    """
    Generate professional two-page PDF tear sheets.

    Pages
    -----
    Page 1
        • Header
        • KPI Tiles
        • Revenue Chart
        • Net Profit Chart
        • ROE / ROCE Chart

    Page 2
        • Balance Sheet Composition
        • Cash Flow Waterfall
        • Pros
        • Cons
        • Capital Allocation Badge
    """

    def __init__(
        self,
        companies_df: pd.DataFrame,
        profitloss_df: pd.DataFrame,
        balancesheet_df: pd.DataFrame,
        cashflow_df: pd.DataFrame,
        proscons_df: pd.DataFrame,
        cashflow_intelligence_df: pd.DataFrame,
        output_dir,
    ):
        """
        Parameters
        ----------
        companies_df
        profitloss_df
        balancesheet_df
        cashflow_df
        proscons_df
        cashflow_intelligence_df
        output_dir
        """

        self.companies_df = companies_df.copy()

        self.pnl_df = profitloss_df.copy()

        self.balance_df = balancesheet_df.copy()

        self.cashflow_df = cashflow_df.copy()

        self.proscons_df = proscons_df.copy()

        self.intelligence_df = cashflow_intelligence_df.copy()

        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        logger.info(
            "Company Tear Sheet initialized."
        )

        self.styles = getSampleStyleSheet()

        self.styles.add(
            ParagraphStyle(
                name="CompanyTitle",
                parent=self.styles["Heading1"],
                fontSize=20,
                leading=24,
                textColor=colors.HexColor("#1F4E79"),
                alignment=TA_CENTER,
                spaceAfter=12,
            )
        )
        # --------------------------------------------------
        # Subtitle
        # --------------------------------------------------

        self.styles.add(
            ParagraphStyle(
                name="Subtitle",
                parent=self.styles["Heading2"],
                fontSize=12,
                leading=15,
                alignment=TA_CENTER,
                textColor=colors.grey,
                spaceAfter=10,
            )
        )       
        # --------------------------------------------------
        # Heading
        # --------------------------------------------------

        self.styles.add(
            ParagraphStyle(
                name="Heading",
                parent=self.styles["Heading2"],
                fontSize=14,
                leading=18,
                textColor=HexColor("#1F4E79"),
                spaceBefore=8,
                spaceAfter=6,
            )
        )

        # --------------------------------------------------
        # Section Heading
        # --------------------------------------------------

        self.styles.add(
            ParagraphStyle(
                name="SectionHeading",
                parent=self.styles["Heading2"],
                fontSize=13,
                leading=16,
                textColor=HexColor("#1F4E79"),
                spaceBefore=8,
                spaceAfter=6,
            )
        )

        # --------------------------------------------------
        # Chart Heading
        # --------------------------------------------------

        self.styles.add(
            ParagraphStyle(
                name="ChartHeading",
                parent=self.styles["Heading2"],
                fontSize=12,
                leading=15,
                alignment=TA_CENTER,
                textColor=HexColor("#0B5394"),
                spaceAfter=8,
            )
        )

        # --------------------------------------------------
        # Body
        # --------------------------------------------------

        self.styles.add(
            ParagraphStyle(
                name="Body",
                parent=self.styles["BodyText"],
                fontSize=10,
                leading=14,
                alignment=TA_LEFT,
                textColor=colors.black,
            )
        )

        # --------------------------------------------------
        # Footer
        # --------------------------------------------------

        self.styles.add(
            ParagraphStyle(
                name="Footer",
                parent=self.styles["BodyText"],
                fontSize=8,
                leading=10,
                alignment=TA_RIGHT,
                textColor=colors.grey,
            )
        )
    # ---------------------------------------------------------
    # Data Helper Methods
    # ---------------------------------------------------------
    @staticmethod
    def clean_year_axis(df: pd.DataFrame) -> pd.DataFrame:
        """
            Convert year column to datetime, remove invalid rows,
            sort chronologically, and keep the latest 10 years.
        """
        df = df.copy()

        df["year_dt"] = pd.to_datetime(
                df["year"],format="mixed",
                errors="coerce",
           )

        df = (
                df.dropna(subset=["year_dt"])
                .sort_values("year_dt")
                .tail(10)
                .reset_index(drop=True)
        )

        return df
    def _company_info(self, company_id):
        """
        Return company master record.
        """

        df = self.companies_df[
            self.companies_df["company_id"] == company_id
        ]

        if df.empty:
            return None

        return df.iloc[0]


    def _profitloss(self, company_id):
        """
        Return company profit & loss history.
        """
        
        df = self.pnl_df[
            self.pnl_df["company_id"] == company_id
    ]

        return (
            df.copy()
            .sort_values("year")
        )


    def _balancesheet(self, company_id):
        """
        Return balance sheet history.
        """

        return (
            self.balance_df[
                self.balance_df["company_id"] == company_id
            ]
            .copy()
            .sort_values("year")
        )


    def _cashflow(self, company_id):
        """
        Return cash flow history.
        """

        return (
            self.cashflow_df[
                self.cashflow_df["company_id"] == company_id
            ]
            .copy()
            .sort_values("year")
        )


    def _pros_cons(self, company_id):
        """
        Return Pros & Cons dataframe.
        """

        return self.proscons_df[
            self.proscons_df["company_id"] == company_id
        ].copy()


    def _intelligence(self, company_id):
        """
        Return Cash Flow Intelligence row.
        """

        df = self.intelligence_df[
            self.intelligence_df["company_id"] == company_id
        ]

        if df.empty:
            return None

        return df.iloc[0]


    # ---------------------------------------------------------
# Header
# ---------------------------------------------------------

    def _header_table(
        self,
        company_name,
        ticker,
        sector,
    ):

        title = Paragraph(
            f"<b>{company_name}</b>",
            TITLE_STYLE,
        )

        subtitle = Paragraph(
            f"{ticker} | {sector}",
            SUBTITLE_STYLE,
        )

        table = Table(

            [[title],
            [subtitle]],

            colWidths=[9.8 * inch],

        )

        table.setStyle(

            TableStyle([

                ("BACKGROUND",
                (0, 0),
                (-1, -1),
                NAVY),

                ("LEFTPADDING",
                (0, 0),
                (-1, -1),
                12),

                ("RIGHTPADDING",
                (0, 0),
                (-1, -1),
                12),

                ("TOPPADDING",
                (0, 0),
                (-1, -1),
                10),

                ("BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                10),

            ])

        )

        return table

    # ---------------------------------------------------------
    # KPI Tile
    # ---------------------------------------------------------

    def _kpi_tile(
        self,
        title,
        value,
    ):

        data = [

            [
                Paragraph(
                    title,
                    KPI_TITLE_STYLE,
                )
            ],

            [
                Paragraph(
                    str(value),
                    KPI_VALUE_STYLE,
                )
            ],

        ]

        table = Table(

            data,

            colWidths=[KPI_TILE_WIDTH],

            rowHeights=[
                0.30 * inch,
                0.50 * inch,
            ],

        )

        table.setStyle(

            TableStyle([

                ("BACKGROUND",
                (0, 0),
                (-1, -1),
                LIGHT_GRAY),

                ("GRID",
                (0, 0),
                (-1, -1),
                0.25,
                BORDER),

                ("VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"),

                ("ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"),

            ])

        )

        return table

    # ---------------------------------------------------------
    # Capital Allocation Badge
    # ---------------------------------------------------------

    def _capital_badge(
    self,
    label,
    ):

        colour = BLUE

        if label == "Expansion":
            colour = GREEN

        elif label == "Debt Reduction":
            colour = ORANGE

        elif label == "Balanced":
            colour = NAVY

        elif label == "Liquidating Assets":
            colour = RED

        badge = Table(

            [[
                Paragraph(
                    f"<b>{label}</b>",
                    SUBTITLE_STYLE,
                )
            ]],

            colWidths=[2.2 * inch],

        )

        badge.setStyle(

            TableStyle([

                ("BACKGROUND",
                (0, 0),
                (-1, -1),
                colour),

                ("ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"),

                ("VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"),

                ("BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8),

                ("TOPPADDING",
                (0, 0),
                (-1, -1),
                8),

            ])

        )

        return badge
    # ---------------------------------------------------------
# Word Wrap Table
# ---------------------------------------------------------

    def _wordwrap_table(
        self,
        dataframe,
    ):

        headers = [

            Paragraph(
                f"<b>{c}</b>",
                BODY_STYLE,
            )

            for c in dataframe.columns

        ]

        rows = []

        for _, row in dataframe.iterrows():

            rows.append(

                [

                    Paragraph(
                        str(value),
                        BODY_STYLE,
                    )

                    for value in row

                ]

            )

        col_width = 7.5 * inch / len(dataframe.columns)

        table = Table(
            [headers] + rows,
            colWidths=[col_width] * len(dataframe.columns),
            repeatRows=1,
        )

        table.setStyle(

            TableStyle([

                ("GRID",
                (0, 0),
                (-1, -1),
                0.25,
                BORDER),

                ("BACKGROUND",
                (0, 0),
                (-1, 0),
                LIGHT_GRAY),

                ("VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"),

            ])

        )

        return table
    
    # ---------------------------------------------------------
    # Pros
    # ---------------------------------------------------------

    def _pros_list(self, items):

        story = []

        for item in items:

           if pd.notna(item):
                story.append(
                    Paragraph(str(item), GOOD_STYLE, bulletText="•")
            )

            

        return story


    # ---------------------------------------------------------
    # Cons
    # ---------------------------------------------------------

    def _cons_list(self, items):

        story = []

        for item in items:

            if pd.notna(item):
                story.append(
                Paragraph(str(item), BAD_STYLE, bulletText="•")
    )
        return story

    # ---------------------------------------------------------
    # Revenue Chart (10 Years)
    # ---------------------------------------------------------

    def _revenue_chart(self, company_id):
        """
        Create 10-Year Revenue Bar Chart.

        Returns
        -------
        reportlab.graphics.shapes.Drawing
        """

        df = self._profitloss(company_id)

        if df.empty:
            return Drawing(CHART_WIDTH, CHART_HEIGHT)

        # --------------------------------------------------
        # Clean Data
        # --------------------------------------------------

        df = self.clean_year_axis(df)

        years = (
            df["year_dt"]
            .dt.strftime("%y")
            .fillna("")
            .astype(str)
            .tolist()
        )

        
        revenue_col = None

        candidates = [
            "sales",
            "revenue",
            "total_income",
            "operating_revenue",
            "net_sales"
        ]

        for col in candidates:
            if col in df.columns:
                revenue_col = col
                break

        if revenue_col is None:
            logger.warning(
                f"Revenue column not found for {company_id}"
            )
            return Drawing(CHART_WIDTH, CHART_HEIGHT)

        df[revenue_col] = (
            pd.to_numeric(
                df[revenue_col],
                errors="coerce"
            )
            .fillna(0)
        )

        revenue = (
            df[revenue_col]
            .round(2)
            .tolist()
        )

        drawing = Drawing(
            CHART_WIDTH,
            CHART_HEIGHT
        )

        chart = VerticalBarChart()

        chart.x = 45
        chart.y = 30

        chart.width = 270
        chart.height = 140

        chart.data = [revenue]

        chart.categoryAxis.categoryNames = years

        chart.categoryAxis.labels.angle = 0
        chart.categoryAxis.labels.boxAnchor = "n"

        chart.valueAxis.valueMin = 0

        max_value = max(revenue) if revenue else 1

        chart.valueAxis.valueMax = (
            np.ceil(max_value / 1000) * 1000
        )

        chart.valueAxis.valueStep = (
            chart.valueAxis.valueMax / 5
        )
        # --------------------------------------------------
        # Styling
        # --------------------------------------------------

        chart.bars[0].fillColor = BLUE
        chart.bars[0].strokeColor = NAVY
        chart.bars[0].strokeWidth = 0.5

        chart.categoryAxis.strokeColor = GRAY
        chart.valueAxis.strokeColor = GRAY

        chart.categoryAxis.labels.fontName = "Helvetica"
        chart.categoryAxis.labels.fontSize = 8

        chart.valueAxis.labels.fontName = "Helvetica"
        chart.valueAxis.labels.fontSize = 8

        chart.valueAxis.labels.fillColor = GRAY

        chart.categoryAxis.labels.fillColor = GRAY

        chart.valueAxis.visibleGrid = True
        chart.valueAxis.gridStrokeColor = LIGHT_GRAY
        chart.valueAxis.gridStrokeWidth = 0.35

        chart.barSpacing = 6
        chart.groupSpacing = 10

        drawing.add(chart)

        # --------------------------------------------------
        # Chart Title
        # --------------------------------------------------

        title = String(
            CHART_WIDTH / 2,
            CHART_HEIGHT - 8,
            "Revenue (10 Years)",
            fontName="Helvetica-Bold",
            fontSize=11,
            fillColor=NAVY,
            textAnchor="middle",
        )

        drawing.add(title)

        # --------------------------------------------------
        # Revenue Value Labels
        # --------------------------------------------------

        max_height = chart.height
        max_axis = chart.valueAxis.valueMax

        for i, value in enumerate(revenue):

            if max_axis == 0:
                continue

            x = (
                chart.x
                + chart.groupSpacing
                + (i * (chart.barWidth + chart.barSpacing))
                + chart.barWidth / 2
            )

            y = (
                chart.y
                + (value / max_axis) * max_height
                + 4
            )

            if value >= 1000:
                label = f"{value/1000:.1f}K"
            else:
                label = f"{value:.0f}"

            drawing.add(
            String(
                x,
                y,
                label,
                
            ))
                

            # --------------------------------------------------
            # Outer Border
            # --------------------------------------------------

            drawing.add(
                Rect(
                        0,
                        0,
                        CHART_WIDTH,
                        CHART_HEIGHT,
                        strokeColor=BORDER,
                        strokeWidth=0.5,
                        fillColor=None,
                    )
                )

        return drawing
    # ---------------------------------------------------------
# Net Profit Chart (10 Years)
# ---------------------------------------------------------

    def _net_profit_chart(self, company_id):
        """
        Create 10-Year Net Profit Bar Chart.

        Returns
        -------
        reportlab.graphics.shapes.Drawing
        """

        df = self._profitloss(company_id)

        if df.empty:
            return Drawing(CHART_WIDTH, CHART_HEIGHT)

        # --------------------------------------------------
        # Clean Data
        # --------------------------------------------------

        df = self.clean_year_axis(df)

        profit_col = None

        candidates = [
            "net_profit",
            "profit_after_tax",
            "pat",
            "netprofit",
            "profit"
        ]

        for col in candidates:
            if col in df.columns:
                profit_col = col
                break

        if profit_col is None:
            logger.warning(
                f"Net Profit column not found for {company_id}"
            )
            return Drawing(CHART_WIDTH, CHART_HEIGHT)

        df[profit_col] = (
            pd.to_numeric(
                df[profit_col],
                errors="coerce"
            )
            .fillna(0)
        )

        years = (
            df["year_dt"]
            .dt.strftime("%y")
            .tolist()
        )

        profits = (
            df[profit_col]
            .round(2)
            .tolist()
        )

        drawing = Drawing(
            CHART_WIDTH,
            CHART_HEIGHT
        )

        chart = VerticalBarChart()

        chart.x = 45
        chart.y = 30

        chart.width = 270
        chart.height = 140

        chart.data = [profits]

        chart.categoryAxis.categoryNames = years

        chart.categoryAxis.labels.angle = 0
        chart.categoryAxis.labels.boxAnchor = "n"

        # --------------------------------------------------
        # Axis Scaling
        # --------------------------------------------------

        min_value = min(profits) if profits else 0
        max_value = max(profits) if profits else 1

        if min_value < 0:
            chart.valueAxis.valueMin = np.floor(min_value / 1000) * 1000
        else:
            chart.valueAxis.valueMin = 0

        chart.valueAxis.valueMax = (
            np.ceil(max_value / 1000) * 1000
        )

        if chart.valueAxis.valueMax == chart.valueAxis.valueMin:
            chart.valueAxis.valueMax += 1000

        chart.valueAxis.valueStep = max(
            (chart.valueAxis.valueMax - chart.valueAxis.valueMin) / 5, 1
        )

        # --------------------------------------------------
        # Styling
        # --------------------------------------------------

        chart.bars[0].fillColor = GREEN
        chart.bars[0].strokeColor = NAVY
        chart.bars[0].strokeWidth = 0.5

        chart.categoryAxis.strokeColor = GRAY
        chart.valueAxis.strokeColor = GRAY

        chart.categoryAxis.labels.fontName = "Helvetica"
        chart.categoryAxis.labels.fontSize = 8
        chart.categoryAxis.labels.fillColor = GRAY

        chart.valueAxis.labels.fontName = "Helvetica"
        chart.valueAxis.labels.fontSize = 8
        chart.valueAxis.labels.fillColor = GRAY

        chart.valueAxis.visibleGrid = True
        chart.valueAxis.gridStrokeColor = LIGHT_GRAY
        chart.valueAxis.gridStrokeWidth = 0.35

        chart.barSpacing = 6
        chart.groupSpacing = 10

        drawing.add(chart)

        # --------------------------------------------------
        # Chart Title
        # --------------------------------------------------

        title = String(
            CHART_WIDTH / 2,
            CHART_HEIGHT - 8,
            "Net Profit (10 Years)",
            fontName="Helvetica-Bold",
            fontSize=11,
            fillColor=NAVY,
            textAnchor="middle",
        )

        drawing.add(title)

        # --------------------------------------------------
        # Value Labels
        # --------------------------------------------------

        axis_min = chart.valueAxis.valueMin
        axis_max = chart.valueAxis.valueMax
        axis_range = axis_max - axis_min

        if axis_range == 0:
            axis_range = 1

        for i, value in enumerate(profits):

            x = (
                chart.x
                + chart.groupSpacing
                + (i * (chart.barWidth + chart.barSpacing))
                + chart.barWidth / 2
            )

            y = (
                chart.y
                + ((value - axis_min) / axis_range)
                * chart.height
            )

            if value >= 1000:
                label = f"{value/1000:.1f}K"
            elif value <= -1000:
                label = f"-{abs(value)/1000:.1f}K"
            else:
                label = f"{value:.0f}"

            offset = 6 if value >= 0 else -10

            drawing.add(
                String(
                    x,
                    y + offset,
                    label,
                    fontName="Helvetica",
                    fontSize=6,
                    fillColor=GRAY,
                    textAnchor="middle",
                )
            )

        # --------------------------------------------------
        # Outer Border
        # --------------------------------------------------

        drawing.add(
            Rect(
                0,
                0,
                CHART_WIDTH,
                CHART_HEIGHT,
                strokeColor=BORDER,
                strokeWidth=0.5,
                fillColor=None,
            )
        )

        return drawing

# ---------------------------------------------------------
# ROE vs ROCE Trend Chart
# ---------------------------------------------------------

    def _roe_roce_chart(self, company_id):
        """
        Generate 10-Year ROE vs ROCE trend chart.

        Returns
        -------
        reportlab.graphics.shapes.Drawing
        """

        df = self._company_info(company_id)

        if df is None:
            return Drawing(CHART_WIDTH, CHART_HEIGHT)

        # --------------------------------------------------
        # Load Financial History
        # --------------------------------------------------

        pnl = self._profitloss(company_id)

        if pnl.empty:
            return Drawing(CHART_WIDTH, CHART_HEIGHT)

        pnl = self.clean_year_axis(pnl)

        # --------------------------------------------------
        # Detect Columns
        # --------------------------------------------------

        roe_col = None
        roce_col = None

        roe_candidates = [
            "roe",
            "roe_percentage",
            "return_on_equity",
        ]

        roce_candidates = [
            "roce",
            "roce_percentage",
            "return_on_capital_employed",
        ]

        for col in roe_candidates:
            if col in pnl.columns:
                roe_col = col
                break

        for col in roce_candidates:
            if col in pnl.columns:
                roce_col = col
                break

        # --------------------------------------------------
        # Fallback
        # --------------------------------------------------
        intelligence = self._intelligence(company_id)

        if roe_col is None:

            intelligence = intelligence 

            if (
                intelligence is not None
                and "roe_percentage" in intelligence.index
            ):
                pnl["roe_percentage"] = intelligence["roe_percentage"]
                roe_col = "roe_percentage"

        if roce_col is None:

            intelligence = intelligence 

            if (
                intelligence is not None
                and "roce_percentage" in intelligence.index
            ):
                pnl["roce_percentage"] = intelligence["roce_percentage"]
                roce_col = "roce_percentage"

        if roe_col is None or roce_col is None:

            logger.warning(
                f"ROE / ROCE data unavailable for {company_id}"
            )

            return Drawing(
                CHART_WIDTH,
                CHART_HEIGHT,
            )

        # --------------------------------------------------
        # Clean Values
        # --------------------------------------------------

        pnl[roe_col] = pd.to_numeric(
            pnl[roe_col],
            errors="coerce",
        ).fillna(0)

        pnl[roce_col] = pd.to_numeric(
            pnl[roce_col],
            errors="coerce",
        ).fillna(0)

        years = (
            pnl["year_dt"]
            .dt.strftime("%y")
            .tolist()
        )

        roe = pnl[roe_col].round(2).tolist()

        roce = pnl[roce_col].round(2).tolist()

        # --------------------------------------------------
        # Create Drawing
        # --------------------------------------------------

        drawing = Drawing(
            CHART_WIDTH,
            CHART_HEIGHT,
        )

        chart = HorizontalLineChart()

        chart.x = 45
        chart.y = 30

        chart.width = 270
        chart.height = 140

        chart.data = [
            roe,
            roce,
        ]

        chart.categoryAxis.categoryNames = years

        chart.categoryAxis.labels.fontName = "Helvetica"
        chart.categoryAxis.labels.fontSize = 8

        chart.categoryAxis.labels.angle = 0

        # --------------------------------------------------
        # Y Axis Scaling
        # --------------------------------------------------

        values = roe + roce

        ymin = min(values)
        ymax = max(values)

        chart.valueAxis.valueMin = np.floor(ymin / 5) * 5
        chart.valueAxis.valueMax = np.ceil(ymax / 5) * 5

        if chart.valueAxis.valueMax == chart.valueAxis.valueMin:
            chart.valueAxis.valueMax += 5

        chart.valueAxis.valueStep = (
            chart.valueAxis.valueMax -
            chart.valueAxis.valueMin
        ) / 5
        if not values:
            return Drawing(CHART_WIDTH, CHART_HEIGHT)
        # --------------------------------------------------
        # Chart Styling
        # --------------------------------------------------

        chart.lines[0].strokeColor = BLUE
        chart.lines[0].strokeWidth = 2.2

        chart.lines[1].strokeColor = colors.green
        chart.lines[1].strokeWidth = 2.2

        chart.lines[0].symbol = makeMarker("FilledCircle")
        chart.lines[0].symbol.size = 5
        chart.lines[0].symbol.fillColor = BLUE
        chart.lines[0].symbol.strokeColor = BLUE

        chart.lines[1].symbol = makeMarker("FilledCircle")
        chart.lines[1].symbol.size = 5
        chart.lines[1].symbol.fillColor = colors.green
        chart.lines[1].symbol.strokeColor = colors.green

        # --------------------------------------------------
        # Grid & Axes
        # --------------------------------------------------

        chart.valueAxis.visibleGrid = True
        chart.valueAxis.gridStrokeColor = LIGHT_GRAY
        chart.valueAxis.gridStrokeWidth = 0.4

        chart.valueAxis.labels.fontName = "Helvetica"
        chart.valueAxis.labels.fontSize = 8

        chart.categoryAxis.strokeColor = BORDER
        chart.valueAxis.strokeColor = BORDER

        # --------------------------------------------------
        # Chart Title
        # --------------------------------------------------

        drawing.add(String(
            CHART_WIDTH / 2,
            CHART_HEIGHT - 12,
            "ROE vs ROCE (10 Years)",
            fontName="Helvetica-Bold",
            fontSize=10,
            fillColor=NAVY,
            textAnchor="middle",
        ))

        # --------------------------------------------------
        # Legend
        # --------------------------------------------------

        legend = Legend()

        legend.x = 170
        legend.y = CHART_HEIGHT - 25

        legend.fontName = "Helvetica"
        legend.fontSize = 8

        legend.colorNamePairs = [
            (BLUE, "ROE"),
            (colors.green, "ROCE"),
        ]

        drawing.add(legend)

        # --------------------------------------------------
        # Border
        # --------------------------------------------------

        drawing.add(Rect(
            0,
            0,
            CHART_WIDTH,
            CHART_HEIGHT,
            strokeColor=BORDER,
            fillColor=None,
            strokeWidth=0.6,
        ))

        drawing.add(chart)

        return drawing

    # ---------------------------------------------------------
    # Debt-to-Equity Trend Chart
    # ---------------------------------------------------------
    def _debt_equity_chart(self, company_id):
        """
        Generate 10-Year Debt-to-Equity Trend Chart.

        Returns
        -------
        reportlab.graphics.shapes.Drawing
        """

        df = self._company_info(company_id)

        if df is None:
            return Drawing(CHART_WIDTH, CHART_HEIGHT)

        # --------------------------------------------------
        # Load Balance Sheet
        # --------------------------------------------------

        balance = self._balancesheet(company_id)

        if balance.empty:
            return Drawing(CHART_WIDTH, CHART_HEIGHT)

        balance = self.clean_year_axis(balance)

        # --------------------------------------------------
        # Detect Existing D/E Ratio Column
        # --------------------------------------------------

        de_col = None

        de_candidates = [
            "debt_to_equity",
            "debt_equity_ratio",
            "de_ratio",
            "d/e",
        ]

        for col in de_candidates:
            if col in balance.columns:
                de_col = col
                break

        # --------------------------------------------------
        # Calculate D/E Ratio if Required
        # --------------------------------------------------

        if de_col is None:

            debt_col = None
            equity_col = None

            debt_candidates = [
                "borrowings",
                "total_debt",
                "debt",
                "long_term_borrowings",
                "total_borrowings",
            ]

            equity_candidates = [
                "shareholders_equity",
                "total_equity",
                "equity",
                "net_worth",
            ]

            for col in debt_candidates:
                if col in balance.columns:
                    debt_col = col
                    break

            for col in equity_candidates:
                if col in balance.columns:
                    equity_col = col
                    break

            if debt_col is None or equity_col is None:

                logger.warning(
                    f"Debt/Equity columns unavailable for {company_id}"
                )

                return Drawing(
                    CHART_WIDTH,
                    CHART_HEIGHT,
                )

            balance[debt_col] = pd.to_numeric(
                balance[debt_col],
                errors="coerce",
            ).fillna(0)

            balance[equity_col] = pd.to_numeric(
                balance[equity_col],
                errors="coerce",
            ).replace(0, np.nan)

            balance["de_ratio"] = (
                balance[debt_col] /
                balance[equity_col]
            ).fillna(0)

            de_col = "de_ratio"

        # --------------------------------------------------
        # Prepare Data
        # --------------------------------------------------

        balance[de_col] = pd.to_numeric(
            balance[de_col],
            errors="coerce",
        ).fillna(0)

        years = (
            balance["year_dt"]
            .dt.strftime("%y")
            .tolist()
        )

        de_values = (
            balance[de_col]
            .round(2)
            .tolist()
        )

        # --------------------------------------------------
        # Create Chart
        # --------------------------------------------------

        drawing = Drawing(
            CHART_WIDTH,
            CHART_HEIGHT,
        )

        chart = HorizontalLineChart()

        chart.x = 45
        chart.y = 30

        chart.width = 270
        chart.height = 140

        chart.data = [de_values]

        chart.categoryAxis.categoryNames = years

        chart.categoryAxis.labels.fontName = "Helvetica"
        chart.categoryAxis.labels.fontSize = 8

        # --------------------------------------------------
        # Y-Axis Scaling
        # --------------------------------------------------

        ymin = min(de_values)
        ymax = max(de_values)

        chart.valueAxis.valueMin = max(
            0,
            np.floor(ymin * 2) / 2,
        )

        chart.valueAxis.valueMax = (
            np.ceil(ymax * 2) / 2
        )

        if chart.valueAxis.valueMax == chart.valueAxis.valueMin:
            chart.valueAxis.valueMax += 0.5

        chart.valueAxis.valueStep = (
            chart.valueAxis.valueMax -
            chart.valueAxis.valueMin
        ) / 5
        if not de_values:
            return Drawing(CHART_WIDTH, CHART_HEIGHT)

            # --------------------------------------------------
        # Chart Styling
        # --------------------------------------------------

        chart.lines[0].strokeColor = colors.darkred
        chart.lines[0].strokeWidth = 2.2

        chart.lines[0].symbol = makeMarker("FilledCircle")
        chart.lines[0].symbol.size = 5
        chart.lines[0].symbol.fillColor = colors.darkred
        chart.lines[0].symbol.strokeColor = colors.darkred

        # --------------------------------------------------
        # Grid & Axes
        # --------------------------------------------------

        chart.valueAxis.visibleGrid = True
        chart.valueAxis.gridStrokeColor = LIGHT_GRAY
        chart.valueAxis.gridStrokeWidth = 0.4

        chart.valueAxis.labels.fontName = "Helvetica"
        chart.valueAxis.labels.fontSize = 8

        chart.categoryAxis.strokeColor = BORDER
        chart.valueAxis.strokeColor = BORDER

        # --------------------------------------------------
        # Reference Line (D/E = 1.0)
        # --------------------------------------------------

        if (
            chart.valueAxis.valueMin <= 1.0 <=
            chart.valueAxis.valueMax
        ):
            ref_y = (
                chart.y +
                (
                    (1.0 - chart.valueAxis.valueMin)
                    /
                    (
                        chart.valueAxis.valueMax -
                        chart.valueAxis.valueMin
                    )
                )
                * chart.height
            )

            drawing.add(Line(
                chart.x,
                ref_y,
                chart.x + chart.width,
                ref_y,
                strokeColor=colors.red,
                strokeWidth=0.8,
                strokeDashArray=[3, 2],
            ))

            drawing.add(String(
                chart.x + chart.width + 5,
                ref_y - 3,
                "1.0",
                fontName="Helvetica",
                fontSize=7,
                fillColor=colors.red,
            ))

        # --------------------------------------------------
        # Chart Title
        # --------------------------------------------------

        drawing.add(String(
            CHART_WIDTH / 2,
            CHART_HEIGHT - 12,
            "Debt-to-Equity Trend (10 Years)",
            fontName="Helvetica-Bold",
            fontSize=10,
            fillColor=NAVY,
            textAnchor="middle",
        ))

        # --------------------------------------------------
        # Legend
        # --------------------------------------------------

        legend = Legend()

        legend.x = 205
        legend.y = CHART_HEIGHT - 25

        legend.fontName = "Helvetica"
        legend.fontSize = 8

        legend.colorNamePairs = [
            (colors.darkred, "Debt / Equity"),
        ]

        drawing.add(legend)

        # --------------------------------------------------
        # Border
        # --------------------------------------------------

        drawing.add(Rect(
            0,
            0,
            CHART_WIDTH,
            CHART_HEIGHT,
            strokeColor=BORDER,
            fillColor=None,
            strokeWidth=0.6,
        ))

        drawing.add(chart)

        return drawing

    # ---------------------------------------------------------
    # Build Page 1 : Header & Company Summary
    # ---------------------------------------------------------

    def _build_header_summary(self, company_id):
        """
        Creates the top section of the company tear sheet.

        Returns
        -------
        list
            ReportLab flowables.
        """

        story = []

        company = self._company_info(company_id)

        if company is None:
            story.append(
                Paragraph(
                    "Company information unavailable.",
                    self.styles["Normal"],
                )
            )
            return story

        # --------------------------------------------------
        # Company Details
        # --------------------------------------------------

        company_name = company.get(
            "company_name",
            company.get("name", company_id),
        )

        symbol = company.get(
            "ticker",
            company.get("symbol", "-"),
        )

        sector = company.get(
            "sector",
            "-",
        )

        industry = company.get(
            "industry",
            "-",
        )

        market_cap = company.get(
            "market_cap",
            "-",
        )

        current_price = company.get(
            "current_price",
            "-",
        )

        high_52 = company.get(
            "high_52_week",
            "-",
        )

        low_52 = company.get(
            "low_52_week",
            "-",
        )

        description = company.get(
            "description",
            "Business description unavailable.",
        )

        # --------------------------------------------------
        # Company Title
        # --------------------------------------------------

        story.append(
            Paragraph(
                f"<b>{company_name}</b>",
                self.styles["CompanyTitle"],
            )
        )

        story.append(
            Paragraph(
                f"{symbol} | {sector} | {industry}",
                self.styles["Subtitle"],
            )
        )

        story.append(
            Spacer(
                1,
                8,
            )
        )

        # --------------------------------------------------
        # Summary Table
        # --------------------------------------------------

        summary_data = [
            [
                "Market Cap",
                market_cap,
                "Current Price",
                current_price,
            ],
            [
                "52W High",
                high_52,
                "52W Low",
                low_52,
            ],
        ]

        summary_table = Table(
            summary_data,
            colWidths=[
                90,
                120,
                90,
                120,
            ],
        )

        summary_table.setStyle(
            TableStyle([
                ("BACKGROUND",(0,0),(-1,0),LIGHT_GRAY),
                ("GRID",(0,0),(-1,-1),0.4,BORDER),
                ("FONTNAME",(0,0),(-1,-1),"Helvetica"),
                ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
                ("FONTNAME",(2,0),(2,-1),"Helvetica-Bold"),
                ("BOTTOMPADDING",(0,0),(-1,-1),6),
                ("TOPPADDING",(0,0),(-1,-1),6),
                ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ])
        )

        story.append(summary_table)

        story.append(
            Spacer(
                1,
                10,
            )
        )

        # --------------------------------------------------
        # Business Description
        # --------------------------------------------------

        story.append(
            Paragraph(
                "<b>Business Summary</b>",
                self.styles["Heading"],
            )
        )

        story.append(
            Paragraph(
                description,
                self.styles["Body"],
            )
        )

        story.append(
            Spacer(
                1,
                12,
            )
        )

        return story

    # ---------------------------------------------------------
    # KPI Tiles
    # ---------------------------------------------------------

    def _build_kpi_tiles(self, company_id):
        """
        Build KPI dashboard tiles.

        Returns
        -------
        reportlab.platypus.Table
        """

        pnl = self._profitloss(company_id)
        balance = self._balancesheet(company_id)
        intelligence = self._intelligence(company_id)

        # --------------------------------------------------
        # Latest Records
        # --------------------------------------------------

        pnl = self.clean_year_axis(pnl)

        if pnl.empty:
            pnl = pd.Series(dtype=object)
        else:
            pnl = pnl.iloc[-1]

        balance = self.clean_year_axis(balance)
        if  balance.empty:  
            balance = pd.Series(dtype=object)          
        else:
            balance = balance.iloc[-1]

        # --------------------------------------------------
        # KPI Values
        # --------------------------------------------------

        revenue = pnl.get(
            "sales",
            pnl.get("revenue", "-"),
        )

        net_profit = pnl.get(
            "net_profit",
            pnl.get("profit_after_tax", "-"),
        )

        eps = pnl.get(
            "eps",
            "-",
        )

        roe = pnl.get(
            "roe",
            intelligence.get("roe_percentage", "-")
            if intelligence is not None else "-",
        )

        roce = pnl.get(
            "roce",
            intelligence.get("roce_percentage", "-")
            if intelligence is not None else "-",
        )

        debt_equity = balance.get(
            "debt_to_equity",
            balance.get("de_ratio", "-"),
        )

        current_ratio = balance.get(
            "current_ratio",
            "-",
        )

        dividend_yield = pnl.get(
            "dividend_yield",
            "-",
        )

        # --------------------------------------------------
        # Format Values
        # --------------------------------------------------

        def fmt(value, suffix=""):
            if value in [None, "", "-"] or pd.isna(value):
                return "-"

            try:
                return f"{float(value):,.2f}{suffix}"
            except Exception:
                return str(value)

        revenue = fmt(revenue)
        net_profit = fmt(net_profit)
        eps = fmt(eps)

        roe = fmt(roe, "%")
        roce = fmt(roce, "%")

        debt_equity = fmt(debt_equity)
        current_ratio = fmt(current_ratio)
        dividend_yield = fmt(dividend_yield, "%")

        # --------------------------------------------------
        # KPI Tiles
        # --------------------------------------------------

        data = [
            [
                self._kpi_tile("Revenue", revenue),
                self._kpi_tile("Net Profit", net_profit),
                self._kpi_tile("EPS", eps),
                self._kpi_tile("ROE", roe),
            ],
            [
                self._kpi_tile("ROCE", roce),
                self._kpi_tile("Debt/Equity", debt_equity),
                self._kpi_tile("Current Ratio", current_ratio),
                self._kpi_tile("Dividend Yield", dividend_yield),
            ],
        ]

        table = Table(
            data,
            colWidths=[
                125,
                125,
                125,
                125,
            ],
            rowHeights=[
                65,
                65,
            ],
        )

        table.setStyle(
            TableStyle([
                ("VALIGN",(0,0),(-1,-1),"TOP"),
                ("ALIGN",(0,0),(-1,-1),"CENTER"),
                ("LEFTPADDING",(0,0),(-1,-1),6),
                ("RIGHTPADDING",(0,0),(-1,-1),6),
                ("TOPPADDING",(0,0),(-1,-1),6),
                ("BOTTOMPADDING",(0,0),(-1,-1),6),
            ])
        )

        return table    

# ---------------------------------------------------------
# Charts Dashboard (2 × 2 Layout)
# ---------------------------------------------------------

    def _build_charts_section(self, company_id):
        """
        Build the charts section for Page-1.

        Layout
        ------
        Revenue        | Net Profit
        ---------------+----------------
        ROE vs ROCE    | Debt/Equity
        """

        # --------------------------------------------------
        # Generate Charts
        # --------------------------------------------------

        revenue_chart = self._revenue_chart(company_id)

        profit_chart = self._net_profit_chart(company_id)

        roe_roce_chart = self._roe_roce_chart(company_id)

        debt_chart = self._debt_equity_chart(company_id)

        # --------------------------------------------------
        # Chart Titles
        # --------------------------------------------------

        revenue_block = [
            Paragraph(
                "<b>Revenue Trend</b>",
                self.styles["ChartHeading"],
            ),
            Spacer(1,4),
            revenue_chart,
        ]

        profit_block = [
            Paragraph(
                "<b>Net Profit Trend</b>",
                self.styles["ChartHeading"],
            ),
            Spacer(1,4),
            profit_chart,
        ]

        roe_block = [
            Paragraph(
                "<b>ROE vs ROCE</b>",
                self.styles["ChartHeading"],
            ),
            Spacer(1,4),
            roe_roce_chart,
        ]

        debt_block = [
            Paragraph(
                "<b>Debt-to-Equity</b>",
                self.styles["ChartHeading"],
            ),
            Spacer(1,4),
            debt_chart,
        ]

        # --------------------------------------------------
        # Arrange Charts
        # --------------------------------------------------

        charts_table = Table(
            [
                [
                    revenue_block,
                    profit_block,
                ],
                [
                    roe_block,
                    debt_block,
                ],
            ],
            colWidths=[
                255,
                255,
            ],
            rowHeights=[
                210,
                210,
            ],
        )

        charts_table.setStyle(
            TableStyle([
                ("VALIGN",(0,0),(-1,-1),"TOP"),
                ("ALIGN",(0,0),(-1,-1),"CENTER"),

                ("GRID",(0,0),(-1,-1),0.4,LIGHT_GRAY),

                ("BOX",(0,0),(-1,-1),0.8,BORDER),

                ("LEFTPADDING",(0,0),(-1,-1),8),
                ("RIGHTPADDING",(0,0),(-1,-1),8),

                ("TOPPADDING",(0,0),(-1,-1),8),
                ("BOTTOMPADDING",(0,0),(-1,-1),8),

                ("BACKGROUND",(0,0),(-1,-1),colors.white),
            ])
        )

        return charts_table

    # ---------------------------------------------------------
    # Financial Health Section
    # ---------------------------------------------------------

    def _build_financial_health(self, company_id):
        """
        Build Pros, Cons, Cash Flow Intelligence,
        Capital Allocation and Overall Rating.
        """

        story = []

        intelligence = self._intelligence(company_id)
        proscons = self._pros_cons(company_id)

        # --------------------------------------------------
        # Pros & Cons
        # --------------------------------------------------

        pros = []
        cons = []

        if not proscons.empty:

            if "type" in proscons.columns:

                pros = (
                    proscons[
                        proscons["type"]
                        .str.lower()
                        .eq("pro")
                    ]["description"]
                    .dropna()
                    .tolist()
                )

                cons = (
                    proscons[
                        proscons["type"]
                        .str.lower()
                        .eq("con")
                    ]["description"]
                    .dropna()
                    .tolist()
                )

        pros_table = self._pros_list(pros)

        cons_table = self._cons_list(cons)

        # --------------------------------------------------
        # Intelligence
        # --------------------------------------------------

        allocation = "-"
        cfo_quality = "-"
        fcf_conversion = "-"
        capex = "-"

        if intelligence is not None:

            allocation = intelligence.get(
                "capital_allocation_label",
                "-"
            )

            cfo_quality = intelligence.get(
                "cfo_quality_score",
                "-"
            )

            fcf_conversion = intelligence.get(
                "fcf_conversion_rate",
                "-"
            )

            capex = intelligence.get(
                "capex_intensity",
                "-"
            )

        badge = self._capital_badge(
            allocation
        )

        intelligence_table = Table(
            [
                ["Capital Allocation", badge],
                ["CFO Quality", str(cfo_quality)],
                ["FCF Conversion", str(fcf_conversion)],
                ["CapEx Intensity", str(capex)],
            ],
            colWidths=[150,220],
        )

        intelligence_table.setStyle(
            TableStyle([
                ("GRID",(0,0),(-1,-1),0.3,BORDER),
                ("BACKGROUND",(0,0),(0,-1),LIGHT_GRAY),
                ("FONTNAME",(0,0),(-1,-1),"Helvetica"),
                ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),
                ("BOTTOMPADDING",(0,0),(-1,-1),6),
                ("TOPPADDING",(0,0),(-1,-1),6),
            ])
        )

        # --------------------------------------------------
        # Overall Rating
        # --------------------------------------------------

        score = 0

        try:

            if float(cfo_quality) >= 80:
                score += 1

            if float(fcf_conversion) >= 80:
                score += 1

            if float(capex) <= 40:
                score += 1

        except Exception:
            pass

        if score == 3:
            rating = "★★★★★ Excellent"

        elif score == 2:
            rating = "★★★★☆ Good"

        elif score == 1:
            rating = "★★★☆☆ Average"

        else:
            rating = "★★☆☆☆ Weak"

        rating_para = Paragraph(
            f"<b>Overall Financial Health:</b> {rating}",
            self.styles["Heading"],
        )

        layout = Table(
            [
                [
                    pros_table,
                    cons_table,
                ],
                [
                    intelligence_table,
                    rating_para,
                ],
            ],
            colWidths=[260,260],
        )

        layout.setStyle(
            TableStyle([
                ("VALIGN",(0,0),(-1,-1),"TOP"),
                ("BOTTOMPADDING",(0,0),(-1,-1),8),
            ])
        )

        story.append(layout)

        return story

    # ---------------------------------------------------------
    # Generate Company Tear Sheet
    # ---------------------------------------------------------

    def build_company_tearsheet(
        self,
        company_id,
        output_path,
    ):
        """
        Generate a two-page Company Tear Sheet.
        """

        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=18,
            leftMargin=18,
            topMargin=18,
            bottomMargin=18,
        )

        story = []

        # =====================================================
        # PAGE 1
        # =====================================================

        story.extend(
            self._build_header_summary(company_id)
        )

        story.append(
            self._build_kpi_tiles(company_id)
        )

        story.append(
            Spacer(1,10)
        )

        story.append(
            self._build_charts_section(company_id)
        )

        story.append(
            Spacer(1,10)
        )

        story.extend(
            self._build_financial_health(company_id)
        )

        # =====================================================
        # PAGE BREAK
        # =====================================================

        story.append(PageBreak())

        # =====================================================
        # PAGE 2
        # =====================================================

        story.append(
            Paragraph(
                "Financial Statements Summary",
                self.styles["SectionHeading"],
            )
        )

        story.append(
            Spacer(1,8)
        )

        story.append(
            self._wordwrap_table(
                self._profitloss(company_id).tail(10)
            )
        )

        story.append(
            Spacer(1,10)
        )

        story.append(
            self._wordwrap_table(
                self._balancesheet(company_id).tail(10)
            )
        )

        story.append(
            Spacer(1,10)
        )

        story.append(
            self._wordwrap_table(
                self._cashflow(company_id).tail(10)
            )
        )

        story.append(
            Spacer(1,12)
        )

        story.append(
            Paragraph(
                "<b>Generated by N100 Financial Intelligence Platform</b>",
                self.styles["Footer"],
            )
        )

        # =====================================================
        # EXPORT
        # =====================================================

        doc.build(story)

        logger.info(
            f"Tear sheet generated: {output_path}"
        )

        return output_path







    
















































































































































