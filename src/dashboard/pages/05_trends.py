"""
=========================================================
Trend Analysis
N100 Financial Intelligence Platform
=========================================================
"""

# =========================================================
# Imports
# =========================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from components.theme import (
    apply_theme,
    page_header,
    section_header
)

from utils.db import (
    get_companies,
    get_pl,
    get_ratios,
    get_cf
)

# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Trend Analysis",
    page_icon="📈",
    layout="wide"
)

apply_theme()

page_header(
    "📈 Trend Analysis",
    "Analyze the historical financial performance of any company."
)

# =========================================================
# Load Company Master
# =========================================================

companies_df = get_companies()

if companies_df.empty:

    st.error("Company master data not found.")
    st.stop()

companies_df = companies_df.sort_values(
    by="company_name"
)

company_list = companies_df["company_name"].tolist()

# =========================================================
# Company Search
# =========================================================

selected_company = st.selectbox(
    "Select Company",
    company_list,
    index=0
)

company_id = companies_df.loc[
    companies_df["company_name"] == selected_company,
    "company_id"
].iloc[0]

# =========================================================
# Load Historical Data
# =========================================================

ratio_df = get_ratios(company_id)

pl_df = get_pl(company_id)

cf_df = get_cf(company_id)

# =========================================================
# Validate Data
# =========================================================

if ratio_df.empty:

    st.warning("Financial ratio data unavailable.")
    st.stop()

if pl_df.empty:

    st.warning("Profit & Loss data unavailable.")
    st.stop()

if cf_df.empty:

    st.warning("Cash Flow data unavailable.")
    st.stop()

# =========================================================
# Data Preparation
# =========================================================

ratio_df = ratio_df.sort_values(
    by="year"
).reset_index(drop=True)

pl_df = pl_df.sort_values(
    by="year"
).reset_index(drop=True)

cf_df = cf_df.sort_values(
    by="year"
).reset_index(drop=True)

# Keep only the latest 10 years

ratio_df = ratio_df.tail(10).reset_index(drop=True)

pl_df = pl_df.tail(10).reset_index(drop=True)

cf_df = cf_df.tail(10).reset_index(drop=True)

# =========================================================
# Create Master Trend DataFrame
# =========================================================

trend_df = pd.merge(
    pl_df,
    ratio_df,
    on=[
        "company_id",
        "year"
    ],
    how="inner"
)

trend_df = pd.merge(
    trend_df,
    cf_df,
    on=[
        "company_id",
        "year"
    ],
    how="left"
)

trend_df = trend_df.sort_values(
    by="year"
).reset_index(drop=True)

# =========================================================
# Verify Trend Dataset
# =========================================================

if trend_df.empty:

    st.warning("No trend data available for the selected company.")
    st.stop()

# =========================================================
# Metric Selection
# =========================================================

section_header("Trend Configuration")

metric_mapping = {

    "Revenue": "sales",

    "Operating Profit": "operating_profit",

    "Net Profit": "net_profit",

    "Operating Margin (%)": "operating_profit_margin_pct",

    "Net Profit Margin (%)": "net_profit_margin_pct",

    "ROE (%)": "return_on_equity_pct",

    "ROCE (%)": "return_on_capital_employed_pct",

    "EPS": "eps",

    "Revenue CAGR (5Y)": "revenue_cagr_5yr",

    "PAT CAGR (5Y)": "pat_cagr_5yr",

    "Debt / Equity": "debt_to_equity",

    "Dividend Yield (%)": "dividend_yield",

    "Free Cash Flow": "free_cash_flow"

}

available_metrics = [

    metric

    for metric, column in metric_mapping.items()

    if column in trend_df.columns

]

selected_metrics = st.multiselect(

    "Select up to 3 metrics",

    options=available_metrics,

    default=available_metrics[:1],

    max_selections=3

)

if len(selected_metrics) == 0:

    st.warning("Please select at least one metric.")

    st.stop()

selected_columns = [

    metric_mapping[m]

    for m in selected_metrics

]

# =========================================================
# Time Range Selection
# =========================================================

section_header("Trend Configuration")

col1, col2 = st.columns([3, 1])

with col1:

    selected_metrics = st.multiselect(

        "Select up to 3 metrics",

        options=available_metrics,

        default=available_metrics[:1],

        max_selections=3

    )

with col2:

    selected_period = st.selectbox(

        "Time Range",

        [

            "1 Year",

            "3 Years",

            "5 Years",

            "10 Years"

        ],

        index=3

    )

# =========================================================
# Filter Years
# =========================================================

years = {

    "1 Year": 1,

    "3 Years": 3,

    "5 Years": 5,

    "10 Years": 10

}

trend_filtered = trend_df.tail(

    years[selected_period]

).copy()

# =========================================================
# Smart Trend Chart
# =========================================================

section_header("Financial Trend Analysis")

fig = go.Figure()

# ---------------------------------------------------------
# Determine Metric Scale
# ---------------------------------------------------------

metric_ranges = {}

for metric_name, column_name in zip(

    selected_metrics,

    selected_columns

):

    metric_ranges[column_name] = (

        trend_filtered[column_name].max()

        -

        trend_filtered[column_name].min()

    )

largest = max(metric_ranges.values())

smallest = min(metric_ranges.values())

# Use secondary axis if one metric is much larger

secondary_axis = (

    largest > 10 * smallest

)

# ---------------------------------------------------------
# Add Traces
# ---------------------------------------------------------

for metric_name, column_name in zip(

    selected_metrics,

    selected_columns

):

    use_secondary = (

        secondary_axis

        and

        metric_ranges[column_name] == smallest

    )

    fig.add_trace(

        go.Scatter(

            x=trend_filtered["year"],

            y=trend_filtered[column_name],

            mode="lines+markers",

            name=metric_name,

            yaxis="y2" if use_secondary else "y"

        )

    )

# ---------------------------------------------------------
# Layout
# ---------------------------------------------------------

layout = dict(

    template="plotly_white",

    hovermode="x unified",

    height=650,

    legend=dict(

        orientation="h",

        y=1.05

    ),

    xaxis=dict(

        title="Year"

    ),

    yaxis=dict(

        title="Primary Axis"

    )

)

if secondary_axis:

    layout["yaxis2"] = dict(

        title="Secondary Axis",

        overlaying="y",

        side="right"

    )

fig.update_layout(**layout)

st.plotly_chart(

    fig,

    use_container_width=True

)

# =========================================================
# Latest Metrics
# =========================================================

section_header("Latest Financial Snapshot")

latest = trend_filtered.iloc[-1]

cols = st.columns(len(selected_metrics))

for col, metric_name, column_name in zip(

    cols,

    selected_metrics,

    selected_columns

):

    current = latest[column_name]

    highest = trend_filtered[column_name].max()

    lowest = trend_filtered[column_name].min()

    if len(trend_filtered) > 1:

        previous = trend_filtered.iloc[-2][column_name]

        if previous != 0:

            yoy = (

                (current - previous)

                /

                abs(previous)

            ) * 100

        else:

            yoy = 0

    else:

        yoy = 0

    with col:

        st.metric(

            metric_name,

            f"{current:,.2f}",

            f"{yoy:+.2f}%"

        )

        st.caption(

            f"High : {highest:,.2f}"

        )

        st.caption(

            f"Low : {lowest:,.2f}"

        )

# =========================================================
# YoY Growth Annotation
# =========================================================

section_header("Year-over-Year Growth")

for metric_name, column_name in zip(

    selected_metrics,

    selected_columns

):

    trend_df[f"{column_name}_yoy"] = (

        trend_df[column_name]

        .pct_change()

        .mul(100)

    )

for metric_name, column_name in zip(

    selected_metrics,

    selected_columns

):

    for _, row in trend_df.iterrows():

        if pd.notna(row[f"{column_name}_yoy"]):

            fig.add_annotation(

                x=row["year"],

                y=row[column_name],

                text=f'{row[f"{column_name}_yoy"]:+.1f}%',

                showarrow=True,

                arrowhead=2,

                font=dict(size=10)

            )

fig.update_layout(

    height=700

)

st.plotly_chart(

    fig,

    use_container_width=True
)

# =========================================================
# Growth Summary
# =========================================================

section_header("Financial Growth Summary")

# ---------------------------------------------------------
# Latest Financial Snapshot
# ---------------------------------------------------------

latest = trend_df.iloc[-1]

previous = trend_df.iloc[-2] if len(trend_df) > 1 else latest

col1, col2, col3, col4 = st.columns(4)

with col1:

    revenue_delta = latest["sales"] - previous["sales"]

    st.metric(

        "Revenue",

        f'₹ {latest["sales"]:,.2f} Cr',

        f'{revenue_delta:,.2f}'

    )

with col2:

    profit_delta = latest["net_profit"] - previous["net_profit"]

    st.metric(

        "Net Profit",

        f'₹ {latest["net_profit"]:,.2f} Cr',

        f'{profit_delta:,.2f}'

    )

with col3:

    roe_delta = (
        latest["return_on_equity_pct"] -
        previous["return_on_equity_pct"]
    )

    st.metric(

        "ROE",

        f'{latest["return_on_equity_pct"]:.2f}%',

        f'{roe_delta:+.2f}%'

    )

with col4:

    roce_delta = (
        latest["return_on_capital_employed_pct"] -
        previous["return_on_capital_employed_pct"]
    )

    st.metric(

        "ROCE",

        f'{latest["return_on_capital_employed_pct"]:.2f}%',

        f'{roce_delta:+.2f}%'

    )

# =========================================================
# Growth Statistics
# =========================================================

st.markdown("### Growth Statistics")

stats1, stats2, stats3 = st.columns(3)

with stats1:

    st.info(f"""
    **Revenue CAGR (5Y)**

    {latest['revenue_cagr_5yr']:.2f} %
    """)

with stats2:

    st.info(f"""
    **PAT CAGR (5Y)**

    {latest['pat_cagr_5yr']:.2f} %
    """)

with stats3:

    st.info(f"""
    **Dividend Yield**

    {latest['dividend_yield']:.2f} %
    """)

# =========================================================
# Historical Statistics
# =========================================================

summary = pd.DataFrame({

    "Metric":[

        "Revenue",

        "Net Profit",

        "ROE",

        "ROCE",

        "Free Cash Flow"

    ],

    "Average":[

        trend_df["sales"].mean(),

        trend_df["net_profit"].mean(),

        trend_df["return_on_equity_pct"].mean(),

        trend_df["return_on_capital_employed_pct"].mean(),

        trend_df["free_cash_flow"].mean()

    ],

    "Maximum":[

        trend_df["sales"].max(),

        trend_df["net_profit"].max(),

        trend_df["return_on_equity_pct"].max(),

        trend_df["return_on_capital_employed_pct"].max(),

        trend_df["free_cash_flow"].max()

    ],

    "Minimum":[

        trend_df["sales"].min(),

        trend_df["net_profit"].min(),

        trend_df["return_on_equity_pct"].min(),

        trend_df["return_on_capital_employed_pct"].min(),

        trend_df["free_cash_flow"].min()

    ]

})

st.dataframe(

    summary,

    use_container_width=True,

    hide_index=True

)

# =========================================================
# Export Trend Data
# =========================================================

section_header("Export Trend Data")

export_df = trend_df.copy()

csv = export_df.to_csv(

    index=False

).encode("utf-8")

st.download_button(

    label="📥 Download Trend Analysis",

    data=csv,

    file_name=f"{selected_company}_trend_analysis.csv",

    mime="text/csv"

)

# =========================================================
# Trend Summary
# =========================================================

st.success(

    f"""
    Showing **{len(export_df)} years**
    of historical financial information
    for **{selected_company}**.
    """

)

# =========================================================
# Footer
# =========================================================

st.divider()

left, center, right = st.columns(3)

with left:

    st.caption("N100 Financial Intelligence Platform")

with center:

    st.caption("Trend Analysis Dashboard")

with right:

    st.caption(f"Company : {selected_company}")


