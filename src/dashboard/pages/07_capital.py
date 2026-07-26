"""
=========================================================
Capital Allocation Analysis
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

    page_title="Capital Allocation",

    page_icon="💰",

    layout="wide"

)

apply_theme()

page_header(

    "💰 Capital Allocation",

    "Analyze companies based on capital allocation strategy."

)

# =========================================================
# Load Data
# =========================================================

companies_df = get_companies()

ratios_df = get_all_ratios()

market_cap_df = get_market_cap_all()

if (

    companies_df.empty

    or

    ratios_df.empty

):

    st.error(

        "Required data not available."

    )

    st.stop()

# =========================================================
# Latest Financial Year
# =========================================================

latest_year = ratios_df["year"].max()

ratios_df = (

    ratios_df

    [

        ratios_df["year"]

        ==

        latest_year

    ]

    .copy()

)

# =========================================================
# Merge Data
# =========================================================

capital_df = ratios_df.merge(

    companies_df,

    on="company_id",

    how="left"

)

if "market_cap_crore" not in capital_df.columns:

    capital_df = capital_df.merge(

        market_cap_df,

        on=[

            "company_id",

            "year"

        ],

        how="left"

    )

capital_df.reset_index(

    drop=True,

    inplace=True

)
# =========================================================
# Capital Allocation Classification
# =========================================================

def classify_company(row):

    roe = row["return_on_equity_pct"]

    debt = row["debt_to_equity"]

    dividend = row["dividend_yield"]

    growth = row["revenue_cagr_5yr"]

    if (

        growth >= 15

        and

        dividend < 1

    ):

        return "High Growth"

    elif (

        dividend >= 3

        and

        debt < 1

    ):

        return "Dividend Leader"

    elif (

        debt >= 2

    ):

        return "Highly Leveraged"

    elif (

        roe >= 20

        and

        growth >= 10

    ):

        return "Compounder"

    elif (

        roe < 10

        and

        growth < 5

    ):

        return "Value Opportunity"

    elif (

        debt < 0.5

        and

        growth >= 8

    ):

        return "Conservative Growth"

    elif (

        dividend >= 2

        and

        growth < 5

    ):

        return "Income Stock"

    else:

        return "Balanced"

capital_df["capital_pattern"] = (

    capital_df

    .apply(

        classify_company,

        axis=1

    )

)

# =========================================================
# Pattern Overview
# =========================================================

section_header(

    "Capital Allocation Patterns"

)

pattern_summary = (

    capital_df

    .groupby(

        "capital_pattern",

        as_index=False

    )

    .agg(

        Companies=(

            "company_name",

            "count"

        ),

        Market_Cap=(

            "market_cap_crore",

            "sum"

        )

    )

)

# =========================================================
# Treemap
# =========================================================

fig = px.treemap(

    pattern_summary,

    path=[

        "capital_pattern"

    ],

    values="Market_Cap",

    color="Companies",

    color_continuous_scale="Blues"

)

fig.update_layout(

    template="plotly_white",

    height=700,

    margin=dict(

        t=40,

        l=20,

        r=20,

        b=20

    )

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# =========================================================
# Pattern Statistics
# =========================================================

section_header(

    "Pattern Summary"

)

st.dataframe(

    pattern_summary,

    use_container_width=True,

    hide_index=True

)

# =========================================================
# Pattern Explorer
# =========================================================

section_header("Explore Capital Allocation Pattern")

selected_pattern = st.selectbox(

    "Select Capital Allocation Pattern",

    sorted(capital_df["capital_pattern"].unique())

)

# =========================================================
# Filter Companies
# =========================================================

pattern_df = (

    capital_df

    [

        capital_df["capital_pattern"]

        ==

        selected_pattern

    ]

    .copy()

)

pattern_df = pattern_df.sort_values(

    by="market_cap_crore",

    ascending=False

)

# =========================================================
# Pattern KPI Cards
# =========================================================

company_count = len(pattern_df)

total_market_cap = pattern_df["market_cap_crore"].sum()

median_roe = pattern_df["return_on_equity_pct"].median()

median_growth = pattern_df["revenue_cagr_5yr"].median()

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "Companies",

        company_count

    )

with col2:

    st.metric(

        "Total Market Cap",

        f"₹ {total_market_cap:,.0f} Cr"

    )

with col3:

    st.metric(

        "Median ROE",

        f"{median_roe:.2f}%"

    )

with col4:

    st.metric(

        "Median Revenue CAGR",

        f"{median_growth:.2f}%"

    )

# =========================================================
# Companies in Selected Pattern
# =========================================================

section_header("Companies")

display_df = pattern_df[

    [

        "company_name",

        "broad_sector",

        "market_cap_crore",

        "return_on_equity_pct",

        "debt_to_equity",

        "dividend_yield",

        "revenue_cagr_5yr",

        "capital_pattern"

    ]

].rename(

    columns={

        "company_name":"Company",

        "broad_sector":"Sector",

        "market_cap_crore":"Market Cap (₹ Cr)",

        "return_on_equity_pct":"ROE (%)",

        "debt_to_equity":"Debt / Equity",

        "dividend_yield":"Dividend Yield (%)",

        "revenue_cagr_5yr":"Revenue CAGR (%)",

        "capital_pattern":"Pattern"

    }

)

st.dataframe(

    display_df,

    use_container_width=True,

    hide_index=True

)

# =========================================================
# Top Companies
# =========================================================

section_header("Largest Companies")

top_market_cap = (

    pattern_df

    .sort_values(

        "market_cap_crore",

        ascending=False

    )

    .head(10)

)

fig = px.bar(

    top_market_cap,

    x="company_name",

    y="market_cap_crore",

    color="broad_sector",

    text="market_cap_crore",

    title="Top Companies by Market Capitalization"

)

fig.update_traces(

    texttemplate="%{text:,.0f}",

    textposition="outside"

)

fig.update_layout(

    template="plotly_white",

    height=550,

    xaxis_title="Company",

    yaxis_title="Market Cap (₹ Crore)"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# =========================================================
# Export
# =========================================================

section_header("Export Analysis")

csv = display_df.to_csv(

    index=False

).encode(

    "utf-8"

)

st.download_button(

    label="📥 Download Capital Allocation Analysis",

    data=csv,

    file_name=f"{selected_pattern.lower().replace(' ','_')}_capital_allocation.csv",

    mime="text/csv"

)

# =========================================================
# Footer
# =========================================================

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:

    st.info(

        f"""

        **Pattern**

        {selected_pattern}

        """

    )

with col2:

    st.info(

        f"""

        **Companies**

        {len(pattern_df)}

        """

    )

with col3:

    st.info(

        f"""

        **Financial Year**

        {latest_year}

        """

    )

st.caption(

    "N100 Financial Intelligence Platform • Capital Allocation Dashboard"
)

