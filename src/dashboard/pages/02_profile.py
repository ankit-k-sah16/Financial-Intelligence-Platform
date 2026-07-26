"""
===========================================================
N100 Financial Intelligence Platform

Page 02 : Company Profile
===========================================================
"""

import streamlit as st
import pandas as pd

from src.dashboard.components.theme import (
    apply_theme,
    page_header,
    section_header
)

from src.dashboard.utils.db import (
    get_companies,
    get_ratios
)

from src.dashboard.components.formatters import (
    format_percentage,
    format_market_cap
)

from src.dashboard.components.charts import (
    create_bar_chart,
    create_multi_line_chart,
    create_kpi_card,
    show
)

# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Company Profile",
    page_icon="📈",
    layout="wide"
)

apply_theme()

page_header(
    "📈 Company Profile",
    "Search and analyze any listed company."
)

# =========================================================
# Load Company Master
# =========================================================

@st.cache_data(show_spinner=False)
def load_company_master():

    df = get_companies()

    if df is None:
        return pd.DataFrame()

    return df


companies = load_company_master()

# =========================================================
# Validate Data
# =========================================================

if companies.empty:

    st.error(
        "No company data found. Please load the database first."
    )

    st.stop()

# =========================================================
# Search Dataset
# =========================================================

companies = companies.copy()

companies["company_name"] = (
    companies["company_name"]
    .fillna("")
    .astype(str)
)

companies["nse_profile"] = (
    companies["nse_profile"]
    .fillna("")
    .astype(str)
)

# ---------------------------------------
# Extract NSE Symbol from URL
# Example:
# https://www.nseindia.com/get-quotes/equity?symbol=TCS
# ----------------------------

companies["ticker"] = (

    companies["nse_profile"]

    .str.extract(

        r"symbol=([^&]+)",

        expand=False

    )

    .fillna("")

    .str.upper()

)

# Search Text

companies["search_text"] = (

    companies["company_name"]

    + " ("

    + companies["ticker"]

    + ")"

)

# =========================================================
# Company Search
# =========================================================

section_header("Search Company")

selected_company = st.selectbox(

    "Search by Company Name or NSE Ticker",

    options=companies["search_text"],

    index=None,

    placeholder="Type company name or ticker..."

)

# =========================================================
# Search Validation
# =========================================================

if selected_company is None:

    st.info(

        """
        👈 Search for a company using its **name** or **NSE ticker**.

        Examples:

        • TCS

        • INFY

        • RELIANCE
        """

    )

    st.stop()

# =========================================================
# Selected Company
# =========================================================

company = companies.loc[
    companies["search_text"] == selected_company].iloc[0]


company_id = company["company_id"]

company_name = company["company_name"]

ticker = company["ticker"]

nse_profile = company["nse_profile"]

# =========================================================
# Latest Financial Record
# =========================================================

latest = ( ratios.sort_values("year").iloc[-1])


company_logo = company.get("company_logo", "")

sector = latest.get("broad_sector", "N/A")

sub_sector = latest.get("sub_sector", "N/A")

website = company.get("website", "")

about = company.get("about_company", "No company description available.")

# =========================================================
# Company Profile
# =========================================================

section_header("Company Profile")

left, right = st.columns([1, 4])

# =========================================================
# Company Logo
# =========================================================

with left:

    if (
        isinstance(company_logo, str)
        and company_logo.strip()
    ):

        st.image(

            company_logo,

            width=120

        )

    else:

        st.info("No Logo")

# =========================================================
# Company Information
# =========================================================
with right:

    st.markdown(

        f"## {company_name}"

    )

    st.markdown(

        f"**Sector:** {sector}"

    )

    st.markdown(

        f"**Sub-Sector:** {sub_sector}"

    )

    st.markdown(

        f"**NSE Symbol:** `{ticker}`"

    )

# =========================================================
# Company Links
# =========================================================

    col1, col2 = st.columns(2)

    with col1:

        if (
            isinstance(website, str)
            and website.strip()
        ):

            st.markdown(

                f"🌐 [Company Website]({website})"

            )

    with col2:

        if (
            isinstance(nse_profile, str)
            and nse_profile.strip()
        ):

            st.markdown(

                f"📈 [NSE Profile]({nse_profile})"

            )

# =========================================================
# About Company
# =========================================================

st.markdown("### About Company")

st.info(

    about

)

# =========================================================
# Financial KPI Dashboard
# =========================================================

section_header("Key Financial Indicators")

latest = ratios.sort_values("year").iloc[-1]

# =========================================================
# KPI Cards
# =========================================================

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:

    create_kpi_card(
        title="ROE",
        value=format_percentage(
            latest["return_on_equity_pct"]
        )
    )

with col2:

    create_kpi_card(
        title="ROCE",
        value=format_percentage(
            latest["return_on_capital_employed_pct"]
        )
    )

with col3:

    create_kpi_card(
        title="Net Profit Margin",
        value=format_percentage(
            latest["net_profit_margin_pct"]
        )
    )

with col4:

    create_kpi_card(
        title="Debt / Equity",
        value=f"{latest['debt_to_equity']:.2f}"
    )

with col5:

    create_kpi_card(
        title="Revenue CAGR (5Y)",
        value=format_percentage(
            latest["revenue_cagr_5yr"]
        )
    )

with col6:

    create_kpi_card(
        title="Free Cash Flow",
        value=format_market_cap(
            latest["free_cash_flow_cr"]
        )
    )

# =========================================================
# KPI Summary
# =========================================================

st.caption(
    "Values shown are based on the latest available financial year."
)

# =========================================================
# Revenue & Profit Trends
# =========================================================

section_header("10-Year Financial Performance")

trend_df = ( ratios .sort_values("year") .copy())

# =========================================================
# Prepare Chart Data
# =========================================================

trend_df["year"] = trend_df["year"].astype(str)

chart_data = trend_df[

    [

        "year",

        "sales",

        "net_profit"

    ]

]

# =========================================================
# Revenue & Net Profit Charts
# =========================================================

col1, col2 = st.columns(2)

with col1:

    fig = create_bar_chart(

        df=chart_data,

        x="year",

        y="sales",

        title="Revenue (10 Years)",

        x_title="Financial Year",

        y_title="Revenue"

    )

    show(fig)

with col2:

    fig = create_bar_chart(

        df=chart_data,

        x="year",

        y="net_profit",

        title="Net Profit (10 Years)",

        x_title="Financial Year",

        y_title="Net Profit"

    )

    show(fig)

# =========================================================
# Financial Trend Summary
# =========================================================

latest_revenue = trend_df.iloc[-1]["sales"]
latest_profit = trend_df.iloc[-1]["net_profit"]

col1, col2 = st.columns(2)

with col1:

    st.metric(

        label="Latest Revenue",

        value=format_market_cap(latest_revenue)

    )

with col2:

    st.metric(

        label="Latest Net Profit",

        value=format_market_cap(latest_profit)

    )

# =========================================================
# PART 5 : ROE vs ROCE Trend Analysis
# =========================================================

import plotly.graph_objects as go
from plotly.subplots import make_subplots


section_header("ROE vs ROCE Trend (10 Years)")

# ---------------------------------------------------------
# Prepare Data
# ---------------------------------------------------------

performance_df = ( ratios.copy().sort_values("year"))


performance_df = performance_df[

    [

        "year",

        "return_on_equity_pct",

        "return_on_capital_employed_pct"

    ]

].dropna()

performance_df["year"] = performance_df["year"].astype(str)

# ---------------------------------------------------------
# Validate Data
# ---------------------------------------------------------

if performance_df.empty:

    st.warning(

        "ROE / ROCE data is not available."

    )

else:

    # -----------------------------------------------------
    # Create Figure
    # -----------------------------------------------------

    fig = make_subplots(

        specs=[[{"secondary_y": True}]]

    )

    # -----------------------------------------------------
    # ROE
    # -----------------------------------------------------

    fig.add_trace(

        go.Scatter(

            x=performance_df["year"],

            y=performance_df["return_on_equity_pct"],

            mode="lines+markers",

            name="ROE (%)",

            line=dict(width=3),

            marker=dict(size=8)

        ),

        secondary_y=False

    )

    # -----------------------------------------------------
    # ROCE
    # -----------------------------------------------------

    fig.add_trace(

        go.Scatter(

            x=performance_df["year"],

            y=performance_df["return_on_capital_employed_pct"],

            mode="lines+markers",

            name="ROCE (%)",

            line=dict(width=3),

            marker=dict(size=8)

        ),

        secondary_y=True

    )

    # -----------------------------------------------------
    # Layout
    # -----------------------------------------------------

    fig.update_layout(

        title="ROE vs ROCE (10-Year Trend)",

        template="plotly_white",

        hovermode="x unified",

        height=500,

        legend=dict(

            orientation="h",

            yanchor="bottom",

            y=1.02,

            xanchor="right",

            x=1

        ),

        margin=dict(

            l=30,

            r=30,

            t=60,

            b=30

        )

    )

    fig.update_xaxes(

        title_text="Financial Year",

        showgrid=False

    )

    fig.update_yaxes(

        title_text="ROE (%)",

        secondary_y=False,

        showgrid=True,

        zeroline=False

    )

    fig.update_yaxes(

        title_text="ROCE (%)",

        secondary_y=True,

        showgrid=False,

        zeroline=False

    )

    # -----------------------------------------------------
    # Display Chart
    # -----------------------------------------------------

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    # -----------------------------------------------------
    # Latest Metrics
    # -----------------------------------------------------

    latest = performance_df.iloc[-1]

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Latest ROE",

            f"{latest['return_on_equity_pct']:.2f}%"

        )

    with col2:

        st.metric(

            "Latest ROCE",

            f"{latest['return_on_capital_employed_pct']:.2f}%"

        )

# =========================================================
# Pros & Cons Analysis
# =========================================================

section_header("Pros & Cons")

# =========================================================
# Load Pros & Cons
# =========================================================

pros_cons_df = get_pros_cons(company_id)

# =========================================================
# Validate Data
# =========================================================

if pros_cons_df.empty:

    st.info(

        "No Pros & Cons available for this company."

    )

else:

    # -----------------------------------------------------
    # Normalize Type Column
    # -----------------------------------------------------

    pros_cons_df["type"] = (

        pros_cons_df["type"]

        .astype(str)

        .str.strip()

        .str.lower()

    )

    # -----------------------------------------------------
    # Split Pros & Cons
    # -----------------------------------------------------

    pros = pros_cons_df.loc[

        pros_cons_df["type"] == "pro",

        "description"

    ].dropna().tolist()

    cons = pros_cons_df.loc[

        pros_cons_df["type"] == "con",

        "description"

    ].dropna().tolist()

    # -----------------------------------------------------
    # Layout
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    # =====================================================
    # Pros
    # =====================================================

    with col1:

        st.success("### ✅ Strengths")

        if len(pros) == 0:

            st.write("No strengths available.")

        else:

            for item in pros:

                st.markdown(

                    f"""
                    <div style="
                        background-color:#eaf7ea;
                        border-left:6px solid #28a745;
                        padding:10px;
                        margin-bottom:10px;
                        border-radius:8px;
                    ">
                        ✅ {item}
                    </div>
                    """,

                    unsafe_allow_html=True

                )

    # =====================================================
    # Cons
    # =====================================================

    with col2:

        st.error("### ❌ Weaknesses")

        if len(cons) == 0:

            st.write("No weaknesses available.")

        else:

            for item in cons:

                st.markdown(

                    f"""
                    <div style="
                        background-color:#fdeaea;
                        border-left:6px solid #dc3545;
                        padding:10px;
                        margin-bottom:10px;
                        border-radius:8px;
                    ">
                        ❌ {item}
                    </div>
                    """,

                    unsafe_allow_html=True

                )

    

   

   

