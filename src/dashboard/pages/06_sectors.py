"""
=========================================================
Sector Analysis
N100 Financial Intelligence Platform
=========================================================
"""

# =========================================================
# Imports
# =========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from components.theme import (
    apply_theme,
    page_header,
    section_header
)

from utils.db import (
    get_companies,
    get_all_ratios,
    get_market_cap_all
)

# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Sector Analysis",
    page_icon="🏭",
    layout="wide"
)

apply_theme()

page_header(
    "🏭 Sector Analysis",
    "Compare companies across sectors using interactive visualizations."
)

# =========================================================
# Load Data
# =========================================================

companies_df = get_companies()

ratios_df = get_all_ratios()

market_cap_df = get_market_cap_all()

# =========================================================
# Validate Data
# =========================================================

if companies_df.empty:

    st.error("Company master data not found.")

    st.stop()

if ratios_df.empty:

    st.error("Financial ratio data not found.")

    st.stop()

if market_cap_df.empty:

    st.error("Market capitalization data not found.")

    st.stop()

# =========================================================
# Keep Latest Financial Year
# =========================================================

latest_year = ratios_df["year"].max()

ratios_df = (

    ratios_df

    [ratios_df["year"] == latest_year]

    .copy()

)

# =========================================================
# Merge Datasets
# =========================================================

sector_df = (

    ratios_df.merge(

        companies_df,

        on="company_id",

        how="left"

    )

)

if "market_cap_crore" not in sector_df.columns:

    sector_df = sector_df.merge(

        market_cap_df,

        on=["company_id", "year"],

        how="left"

    )

# =========================================================
# Required Columns
# =========================================================

required_columns = [

    "company_id",

    "company_name",

    "broad_sector",

    "sub_sector",

    "sales",

    "return_on_equity_pct",

    "market_cap_crore"

]

missing_columns = [

    col

    for col in required_columns

    if col not in sector_df.columns

]

if missing_columns:

    st.error(

        f"Missing columns: {', '.join(missing_columns)}"

    )

    st.stop()

# =========================================================
# Data Cleaning
# =========================================================

numeric_columns = [

    "sales",

    "return_on_equity_pct",

    "market_cap_crore"

]

for col in numeric_columns:

    sector_df[col] = pd.to_numeric(

        sector_df[col],

        errors="coerce"

    )

sector_df = sector_df.dropna(

    subset=numeric_columns

)

sector_df = sector_df.reset_index(

    drop=True

)

# =========================================================
# Sector Selection
# =========================================================

section_header("Sector Selection")

sector_list = (

    sector_df["broad_sector"]

    .dropna()

    .sort_values()

    .unique()

    .tolist()

)

selected_sector = st.selectbox(

    "Select Sector",

    sector_list,

    index=0

)

# =========================================================
# Filter Selected Sector
# =========================================================

filtered_df = (

    sector_df

    [

        sector_df["broad_sector"]

        == selected_sector

    ]

    .copy()

)

filtered_df = filtered_df.sort_values(

    by="company_name"

)

filtered_df = filtered_df.reset_index(

    drop=True

)

# =========================================================
# Sector Summary
# =========================================================

st.info(

    f"""

    **Sector:** {selected_sector}

    **Companies:** {len(filtered_df)}

    """

)

# =========================================================
# Validate Filter
# =========================================================

if filtered_df.empty:

    st.warning(

        "No companies found for the selected sector."

    )

    st.stop()

# =========================================================
# Sector Overview
# =========================================================

section_header("Sector Overview")

# ---------------------------------------------------------
# Calculate KPIs
# ---------------------------------------------------------

company_count = len(filtered_df)

total_revenue = filtered_df["sales"].sum()

median_revenue = filtered_df["sales"].median()

total_market_cap = filtered_df["market_cap_crore"].sum()

median_market_cap = filtered_df["market_cap_crore"].median()

median_roe = filtered_df["return_on_equity_pct"].median()

median_roce = filtered_df["return_on_capital_employed_pct"].median()

median_opm = filtered_df["operating_profit_margin_pct"].median()

# =========================================================
# KPI Cards - Row 1
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        label="Companies",

        value=f"{company_count}"

    )

with col2:

    st.metric(

        label="Total Revenue",

        value=f"₹ {total_revenue:,.0f} Cr"

    )

with col3:

    st.metric(

        label="Median ROE",

        value=f"{median_roe:.2f}%"

    )

with col4:

    st.metric(

        label="Total Market Cap",

        value=f"₹ {total_market_cap:,.0f} Cr"

    )

# =========================================================
# KPI Cards - Row 2
# =========================================================

col5, col6, col7, col8 = st.columns(4)

with col5:

    st.metric(

        label="Median Revenue",

        value=f"₹ {median_revenue:,.0f} Cr"

    )

with col6:

    st.metric(

        label="Median Market Cap",

        value=f"₹ {median_market_cap:,.0f} Cr"

    )

with col7:

    st.metric(

        label="Median ROCE",

        value=f"{median_roce:.2f}%"

    )

with col8:

    st.metric(

        label="Median OPM",

        value=f"{median_opm:.2f}%"

    )


# =========================================================
# Revenue vs ROE Bubble Chart
# =========================================================

section_header("Revenue vs ROE Analysis")

fig = px.scatter(

    filtered_df,

    x="sales",

    y="return_on_equity_pct",

    size="market_cap_crore",

    color="sub_sector",

    hover_name="company_name",

    hover_data={

        "sales": ":,.2f",

        "return_on_equity_pct": ":.2f",

        "market_cap_crore": ":,.2f",

        "sub_sector": True,

        "company_id": True

    },

    title=f"{selected_sector} Sector",

    size_max=60

)

fig.update_layout(

    template="plotly_white",

    height=700,

    legend_title="Sub Sector",

    xaxis_title="Revenue (₹ Crore)",

    yaxis_title="ROE (%)",

    hovermode="closest"

)

fig.update_traces(

    marker=dict(

        opacity=0.80,

        line=dict(

            width=1,

            color="DarkSlateGrey"

        )

    )

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# =========================================================
# Sector Median KPI Analysis
# =========================================================

section_header("Sector Median KPIs")

median_df = pd.DataFrame({

    "Metric":[

        "Revenue",

        "ROE",

        "ROCE",

        "Revenue CAGR",

        "PAT CAGR",

        "OPM",

        "Debt/Equity",

        "Dividend Yield"

    ],

    "Value":[

        filtered_df["sales"].median(),

        filtered_df["return_on_equity_pct"].median(),

        filtered_df["return_on_capital_employed_pct"].median(),

        filtered_df["revenue_cagr_5yr"].median(),

        filtered_df["pat_cagr_5yr"].median(),

        filtered_df["operating_profit_margin_pct"].median(),

        filtered_df["debt_to_equity"].median(),

        filtered_df["dividend_yield"].median()

    ]

})

fig = px.bar(

    median_df,

    x="Metric",

    y="Value",

    text="Value",

    title=f"Median Financial Metrics - {selected_sector}"

)

fig.update_traces(

    texttemplate="%{text:.2f}",

    textposition="outside"

)

fig.update_layout(

    template="plotly_white",

    height=550,

    xaxis_title="Financial Metric",

    yaxis_title="Median Value",

    uniformtext_minsize=10,

    uniformtext_mode="hide"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# =========================================================
# Top & Bottom Performers
# =========================================================

section_header("Sector Leaders & Laggards")

col1, col2 = st.columns(2)

# ---------------------------------------------------------
# Top Performers
# ---------------------------------------------------------

with col1:

    st.subheader("🏆 Top 5 ROE Companies")

    top_df = (

        filtered_df

        .sort_values(

            by="return_on_equity_pct",

            ascending=False

        )

        .head(5)

    )

    st.dataframe(

        top_df[

            [

                "company_name",

                "sales",

                "return_on_equity_pct",

                "market_cap_crore"

            ]

        ].rename(

            columns={

                "company_name": "Company",

                "sales": "Revenue (₹ Cr)",

                "return_on_equity_pct": "ROE (%)",

                "market_cap_crore": "Market Cap (₹ Cr)"

            }

        ),

        use_container_width=True,

        hide_index=True

    )

# ---------------------------------------------------------
# Bottom Performers
# ---------------------------------------------------------

with col2:

    st.subheader("📉 Bottom 5 ROE Companies")

    bottom_df = (

        filtered_df

        .sort_values(

            by="return_on_equity_pct",

            ascending=True

        )

        .head(5)

    )

    st.dataframe(

        bottom_df[

            [

                "company_name",

                "sales",

                "return_on_equity_pct",

                "market_cap_crore"

            ]

        ].rename(

            columns={

                "company_name": "Company",

                "sales": "Revenue (₹ Cr)",

                "return_on_equity_pct": "ROE (%)",

                "market_cap_crore": "Market Cap (₹ Cr)"

            }

        ),

        use_container_width=True,

        hide_index=True

    )

# =========================================================
# Download Sector Data
# =========================================================

section_header("Export Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(

    label="📥 Download Sector Analysis",

    data=csv,

    file_name=f"{selected_sector.lower().replace(' ', '_')}_sector_analysis.csv",

    mime="text/csv"

)

# =========================================================
# Footer Summary
# =========================================================

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:

    st.info(

        f"""

        **Sector**

        {selected_sector}

        """

    )

with col2:

    st.info(

        f"""

        **Companies**

        {len(filtered_df)}

        """

    )

with col3:

    st.info(

        f"""

        **Analysis Year**

        {latest_year}

        """

    )

st.caption(

    "N100 Financial Intelligence Platform • Sector Analysis Dashboard"
)
