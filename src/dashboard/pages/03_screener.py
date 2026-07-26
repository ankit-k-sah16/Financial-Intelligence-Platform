"""
=========================================================
N100 Financial Intelligence Platform
Company Screener
Page 3
=========================================================
"""

# =========================================================
# Imports
# =========================================================

import streamlit as st
import pandas as pd

from utils.db import (
    get_companies,
    get_all_ratios,
    get_sectors
)

from src.dashboard.components.theme import (
    apply_theme,
    page_header,
    section_header
)


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(

    page_title="Company Screener",

    page_icon="🔍",

    layout="wide"

)

apply_theme()

page_header(

    "Company Screener",

    "Filter companies using fundamental financial metrics."

)


# =========================================================
# Load Data
# =========================================================

@st.cache_data

def load_data():

    companies = get_companies()

    ratios = get_all_ratios()

    sectors = get_sectors()

    return companies, ratios, sectors


companies, ratios, sectors = load_data()


# =========================================================
# Validate Data
# =========================================================

if companies.empty:

    st.error(

        "Company master data could not be loaded."

    )

    st.stop()

if ratios.empty:

    st.error(

        "Financial ratio data could not be loaded."

    )

    st.stop()

if sectors.empty:

    st.error(

        "Sector data could not be loaded."

    )

    st.stop()


# =========================================================
# Keep Latest Financial Year
# =========================================================

ratios = (

    ratios

    .sort_values("year")

    .groupby(

        "company_id",

        as_index=False

    ).last()

)


# =========================================================
# Merge Company Data
# =========================================================

screener_df = (

    ratios

    .merge(

        companies,

        on="company_id",

        how="left"

    )

    .merge(

        sectors,

        on="company_id",

        how="left"

    )

)


# =========================================================
# Select Required Columns
# =========================================================

screener_df = screener_df[

    [

        "company_id",

        "company_name",

        "sector",

        "return_on_equity_pct",

        "debt_to_equity",

        "free_cash_flow_cr",

        "revenue_cagr_5yr",

        "pat_cagr_5yr",

        "operating_profit_margin_pct",

        "price_to_earnings",

        "price_to_book",

        "dividend_yield",

        "interest_coverage_ratio"

    ]

]


# =========================================================
# Handle Missing Values
# =========================================================

numeric_columns = [

    "return_on_equity_pct",

    "debt_to_equity",

    "free_cash_flow_cr",

    "revenue_cagr_5yr",

    "pat_cagr_5yr",

    "operating_profit_margin_pct",

    "price_to_earnings",

    "price_to_book",

    "dividend_yield",

    "interest_coverage_ratio"

]

screener_df[numeric_columns] = (

    screener_df[numeric_columns]

    .fillna(0)

)


# =========================================================
# Prepare Dataset
# =========================================================

screener_df = (

    screener_df.sort_values(by="company_name") .reset_index( drop=True )
)


# =========================================================
# Debug Preview (Optional)
# =========================================================

# st.dataframe(screener_df)

# =========================================================
# Sidebar Filters
# =========================================================

st.sidebar.header("🔍 Screening Filters")


# =========================================================
# ROE (Minimum)
# =========================================================

roe_min = st.sidebar.slider(

    "Minimum ROE (%)",

    min_value=float(screener_df["return_on_equity_pct"].min()),

    max_value=float(screener_df["return_on_equity_pct"].max()),

    value=float(screener_df["return_on_equity_pct"].min()),

    step=1.0

)


# =========================================================
# Debt to Equity (Maximum)
# =========================================================

de_max = st.sidebar.slider(

    "Maximum Debt / Equity",

    min_value=float(screener_df["debt_to_equity"].min()),

    max_value=float(screener_df["debt_to_equity"].max()),

    value=float(screener_df["debt_to_equity"].max()),

    step=0.10

)


# =========================================================
# Free Cash Flow (Minimum)
# =========================================================

fcf_min = st.sidebar.slider(

    "Minimum Free Cash Flow (Cr)",

    min_value=float(screener_df["free_cash_flow_cr"].min()),

    max_value=float(screener_df["free_cash_flow_cr"].max()),

    value=float(screener_df["free_cash_flow_cr"].min()),

    step=10.0

)


# =========================================================
# Revenue CAGR (Minimum)
# =========================================================

revenue_cagr_min = st.sidebar.slider(

    "Minimum Revenue CAGR (%)",

    min_value=float(screener_df["revenue_cagr_5yr"].min()),

    max_value=float(screener_df["revenue_cagr_5yr"].max()),

    value=float(screener_df["revenue_cagr_5yr"].min()),

    step=1.0

)


# =========================================================
# PAT CAGR (Minimum)
# =========================================================

pat_cagr_min = st.sidebar.slider(

    "Minimum PAT CAGR (%)",

    min_value=float(screener_df["pat_cagr_5yr"].min()),

    max_value=float(screener_df["pat_cagr_5yr"].max()),

    value=float(screener_df["pat_cagr_5yr"].min()),

    step=1.0

)


# =========================================================
# Operating Profit Margin (Minimum)
# =========================================================

opm_min = st.sidebar.slider(

    "Minimum Operating Profit Margin (%)",

    min_value=float(screener_df["operating_profit_margin_pct"].min()),

    max_value=float(screener_df["operating_profit_margin_pct"].max()),

    value=float(screener_df["operating_profit_margin_pct"].min()),

    step=1.0

)


# =========================================================
# Price to Earnings (Maximum)
# =========================================================

pe_max = st.sidebar.slider(

    "Maximum P/E Ratio",

    min_value=float(screener_df["price_to_earnings"].min()),

    max_value=float(screener_df["price_to_earnings"].max()),

    value=float(screener_df["price_to_earnings"].max()),

    step=1.0

)


# =========================================================
# Price to Book (Maximum)
# =========================================================

pb_max = st.sidebar.slider(

    "Maximum P/B Ratio",

    min_value=float(screener_df["price_to_book"].min()),

    max_value=float(screener_df["price_to_book"].max()),

    value=float(screener_df["price_to_book"].max()),

    step=0.10

)


# =========================================================
# Dividend Yield (Minimum)
# =========================================================

dividend_min = st.sidebar.slider(

    "Minimum Dividend Yield (%)",

    min_value=float(screener_df["dividend_yield"].min()),

    max_value=float(screener_df["dividend_yield"].max()),

    value=float(screener_df["dividend_yield"].min()),

    step=0.10

)


# =========================================================
# Interest Coverage Ratio (Minimum)
# =========================================================

icr_min = st.sidebar.slider(

    "Minimum Interest Coverage Ratio",

    min_value=float(screener_df["interest_coverage_ratio"].min()),

    max_value=float(screener_df["interest_coverage_ratio"].max()),

    value=float(screener_df["interest_coverage_ratio"].min()),

    step=0.50

)

# =========================================================
# Screener Presets
# =========================================================

st.sidebar.markdown("---")

st.sidebar.subheader("📌 Screening Presets")


# =========================================================
# Initialize Session State
# =========================================================

default_filters = {

    "roe_min": float(screener_df["return_on_equity_pct"].min()),

    "de_max": float(screener_df["debt_to_equity"].max()),

    "fcf_min": float(screener_df["free_cash_flow_cr"].min()),

    "revenue_cagr_min": float(screener_df["revenue_cagr_5yr"].min()),

    "pat_cagr_min": float(screener_df["pat_cagr_5yr"].min()),

    "opm_min": float(screener_df["operating_profit_margin_pct"].min()),

    "pe_max": float(screener_df["price_to_earnings"].max()),

    "pb_max": float(screener_df["price_to_book"].max()),

    "dividend_min": float(screener_df["dividend_yield"].min()),

    "icr_min": float(screener_df["interest_coverage_ratio"].min())

}

for key, value in default_filters.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# Quality Preset
# =========================================================

if st.sidebar.button("⭐ Quality"):

    st.session_state.roe_min = 20.0

    st.session_state.de_max = 0.50

    st.session_state.fcf_min = 0.0

    st.session_state.revenue_cagr_min = 10.0

    st.session_state.pat_cagr_min = 10.0

    st.session_state.opm_min = 20.0

    st.session_state.pe_max = float(screener_df["price_to_earnings"].max())

    st.session_state.pb_max = float(screener_df["price_to_book"].max())

    st.session_state.dividend_min = 0.0

    st.session_state.icr_min = 5.0


# =========================================================
# Value Preset
# =========================================================

if st.sidebar.button("💰 Value"):

    st.session_state.roe_min = 12.0

    st.session_state.de_max = 1.00

    st.session_state.fcf_min = 0.0

    st.session_state.revenue_cagr_min = 5.0

    st.session_state.pat_cagr_min = 5.0

    st.session_state.opm_min = 10.0

    st.session_state.pe_max = 20.0

    st.session_state.pb_max = 3.0

    st.session_state.dividend_min = 1.5

    st.session_state.icr_min = 3.0


# =========================================================
# Growth Preset
# =========================================================

if st.sidebar.button("📈 Growth"):

    st.session_state.roe_min = 15.0

    st.session_state.de_max = 1.00

    st.session_state.fcf_min = 0.0

    st.session_state.revenue_cagr_min = 15.0

    st.session_state.pat_cagr_min = 15.0

    st.session_state.opm_min = 15.0

    st.session_state.pe_max = float(screener_df["price_to_earnings"].max())

    st.session_state.pb_max = float(screener_df["price_to_book"].max())

    st.session_state.dividend_min = 0.0

    st.session_state.icr_min = 3.0


# =========================================================
# Dividend Preset
# =========================================================

if st.sidebar.button("💵 Dividend"):

    st.session_state.roe_min = 10.0

    st.session_state.de_max = 1.00

    st.session_state.fcf_min = 0.0

    st.session_state.revenue_cagr_min = 5.0

    st.session_state.pat_cagr_min = 5.0

    st.session_state.opm_min = 10.0

    st.session_state.pe_max = 25.0

    st.session_state.pb_max = 5.0

    st.session_state.dividend_min = 2.5

    st.session_state.icr_min = 3.0


# =========================================================
# Debt-Free Preset
# =========================================================

if st.sidebar.button("🛡 Debt-Free"):

    st.session_state.roe_min = 10.0

    st.session_state.de_max = 0.20

    st.session_state.fcf_min = 0.0

    st.session_state.revenue_cagr_min = 5.0

    st.session_state.pat_cagr_min = 5.0

    st.session_state.opm_min = 10.0

    st.session_state.pe_max = float(screener_df["price_to_earnings"].max())

    st.session_state.pb_max = float(screener_df["price_to_book"].max())

    st.session_state.dividend_min = 0.0

    st.session_state.icr_min = 8.0


# =========================================================
# Turnaround Preset
# =========================================================

if st.sidebar.button("🔄 Turnaround"):

    st.session_state.roe_min = 5.0

    st.session_state.de_max = 2.00

    st.session_state.fcf_min = -100.0

    st.session_state.revenue_cagr_min = 5.0

    st.session_state.pat_cagr_min = 5.0

    st.session_state.opm_min = 5.0

    st.session_state.pe_max = float(screener_df["price_to_earnings"].max())

    st.session_state.pb_max = float(screener_df["price_to_book"].max())

    st.session_state.dividend_min = 0.0

    st.session_state.icr_min = 1.5

# =========================================================
# Apply Screener Filters
# =========================================================

filtered_df = screener_df.copy()


# =========================================================
# Apply ROE Filter
# =========================================================

filtered_df = filtered_df[filtered_df["return_on_equity_pct"] >= roe_min]

# =========================================================
# Apply Debt / Equity Filter
# =========================================================

filtered_df = filtered_df[ filtered_df["debt_to_equity"] <= de_max]

# =========================================================
# Apply Free Cash Flow Filter
# =========================================================

filtered_df = filtered_df[ filtered_df["free_cash_flow_cr"] >= fcf_min]

# =========================================================
# Apply Revenue CAGR Filter
# =========================================================

filtered_df = filtered_df[filtered_df["revenue_cagr_5yr"]>= revenue_cagr_min]


# =========================================================
# Apply PAT CAGR Filter
# =========================================================

filtered_df = filtered_df[filtered_df["pat_cagr_5yr"]  >= pat_cagr_min]


# =========================================================
# Apply Operating Profit Margin Filter
# =========================================================

filtered_df = filtered_df[ filtered_df["operating_profit_margin_pct"]  >= opm_min

]

# =========================================================
# Apply Price to Earnings Filter
# =========================================================

filtered_df = filtered_df[ filtered_df["price_to_earnings"]<= pe_max
]


# =========================================================
# Apply Price to Book Filter
# =========================================================

filtered_df = filtered_df[filtered_df["price_to_book"] <= pb_max

]

# =========================================================
# Apply Dividend Yield Filter
# =========================================================

filtered_df = filtered_df[ filtered_df["dividend_yield"]>= dividend_min

]

# =========================================================
# Apply Interest Coverage Ratio Filter
# =========================================================

filtered_df = filtered_df[filtered_df["interest_coverage_ratio"]>= icr_min

]

# =========================================================
# Reset Index
# =========================================================

filtered_df = (filtered_df.reset_index( drop=True  ))

# =========================================================
# Store Result Count
# =========================================================

result_count = len(filtered_df)


# =========================================================
# No Matching Companies
# =========================================================

if result_count == 0:

    st.warning(

        "No companies match the selected screening criteria."

    )

    st.stop()

# =========================================================
# Composite Score Calculation
# =========================================================

section_header("Composite Ranking")


# =========================================================
# Normalize Metrics
# =========================================================

score_df = filtered_df.copy()


# =========================================================
# Positive Metrics
# =========================================================

positive_metrics = [

    "return_on_equity_pct",

    "free_cash_flow_cr",

    "revenue_cagr_5yr",

    "pat_cagr_5yr",

    "operating_profit_margin_pct",

    "dividend_yield",

    "interest_coverage_ratio"

]

for metric in positive_metrics:

    minimum = score_df[metric].min()

    maximum = score_df[metric].max()

    if maximum > minimum:

        score_df[metric + "_score"] = (

            (score_df[metric] - minimum)

            / (maximum - minimum)

        )

    else:

        score_df[metric + "_score"] = 1.0


# =========================================================
# Negative Metrics
# =========================================================

negative_metrics = [

    "debt_to_equity",

    "price_to_earnings",

    "price_to_book"

]

for metric in negative_metrics:

    minimum = score_df[metric].min()

    maximum = score_df[metric].max()

    if maximum > minimum:

        score_df[metric + "_score"] = (

            (maximum - score_df[metric])

            / (maximum - minimum)

        )

    else:

        score_df[metric + "_score"] = 1.0


# =========================================================
# Weighted Composite Score
# =========================================================

score_df["composite_score"] = (

      score_df["return_on_equity_pct_score"] * 20

    + score_df["revenue_cagr_5yr_score"] * 15

    + score_df["pat_cagr_5yr_score"] * 15

    + score_df["free_cash_flow_cr_score"] * 15

    + score_df["operating_profit_margin_pct_score"] * 10

    + score_df["debt_to_equity_score"] * 10

    + score_df["price_to_earnings_score"] * 5

    + score_df["price_to_book_score"] * 5

    + score_df["dividend_yield_score"] * 3

    + score_df["interest_coverage_ratio_score"] * 2

)

score_df["composite_score"] = (

    score_df["composite_score"]

    .round(2)

)


# =========================================================
# Rank Companies
# =========================================================

score_df = (

    score_df

    .sort_values(

        by="composite_score",

        ascending=False

    )

    .reset_index(

        drop=True

    )

)

# =========================================================
# Screener Results
# =========================================================

section_header("Screening Results")


# =========================================================
# Result Count
# =========================================================

st.success(

    f"📊 {len(score_df)} companies match your filters."

)


# =========================================================
# Select Columns
# =========================================================

display_df = score_df[

    [

        "company_id",

        "company_name",

        "sector",

        "composite_score",

        "return_on_equity_pct",

        "debt_to_equity",

        "free_cash_flow_cr",

        "revenue_cagr_5yr",

        "pat_cagr_5yr",

        "operating_profit_margin_pct",

        "price_to_earnings",

        "price_to_book",

        "dividend_yield",

        "interest_coverage_ratio"

    ]

]


# =========================================================
# Rename Columns
# =========================================================

display_df = display_df.rename(

    columns={

        "company_id": "Company ID",

        "company_name": "Company",

        "sector": "Sector",

        "composite_score": "Score",

        "return_on_equity_pct": "ROE (%)",

        "debt_to_equity": "Debt / Equity",

        "free_cash_flow_cr": "FCF (Cr)",

        "revenue_cagr_5yr": "Revenue CAGR (%)",

        "pat_cagr_5yr": "PAT CAGR (%)",

        "operating_profit_margin_pct": "OPM (%)",

        "price_to_earnings": "P/E",

        "price_to_book": "P/B",

        "dividend_yield": "Dividend Yield (%)",

        "interest_coverage_ratio": "ICR"

    }

)


# =========================================================
# Display Table
# =========================================================

st.dataframe(

    display_df,

    use_container_width=True,

    hide_index=True

)

# =========================================================
# Download Screener Results
# =========================================================

section_header("Export Results")


# =========================================================
# Convert DataFrame to CSV
# =========================================================

csv = (

    display_df.to_csv(index=False )

    .encode("utf-8" )

)


# =========================================================
# Download Button
# =========================================================

st.download_button(

    label="📥 Download Results as CSV",

    data=csv,

    file_name="company_screener_results.csv",

    mime="text/csv"

)

# =========================================================
# Footer
# =========================================================

st.markdown("---")


# =========================================================
# Summary
# =========================================================

total_companies = len(screener_df)

filtered_companies = len(score_df)


# =========================================================
# Footer Message
# =========================================================

st.caption(

    f"Showing {filtered_companies} of {total_companies} companies."

)