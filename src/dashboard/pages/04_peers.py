"""
=========================================================
Peer Comparison
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
    get_peer_groups,
    get_peer_comparison
)

# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Peer Comparison",
    page_icon="📊",
    layout="wide"
)

apply_theme()

page_header(
    "📊 Peer Comparison",
    "Compare a company with its industry peers."
)

# =========================================================
# Load Peer Groups
# =========================================================

peer_groups = get_peer_groups()

if peer_groups.empty:

    st.warning("No peer groups found.")
    st.stop()

peer_group_list = (
    peer_groups["peer_group_name"]
    .dropna()
    .sort_values()
    .unique()
    .tolist()
)

# =========================================================
# Peer Group Selection
# =========================================================

section_header("Peer Group Selection")

selected_group = st.selectbox(
    "Select Peer Group",
    peer_group_list,
    index=0
)

# =========================================================
# Load Companies
# =========================================================

peer_df = get_peer_comparison(selected_group)

if peer_df.empty:

    st.warning("No companies found for this peer group.")
    st.stop()

peer_df = peer_df.sort_values(
    by="company_name"
)

company_list = peer_df["company_name"].tolist()

# =========================================================
# Company Selection
# =========================================================

selected_company = st.selectbox(
    "Select Company",
    company_list,
    index=0
)

company_data = peer_df[
    peer_df["company_name"] == selected_company
].iloc[0]

# =========================================================
# Radar Chart
# =========================================================

section_header("Peer Performance Radar")

metrics = [

    "return_on_equity_pct",

    "return_on_capital_employed_pct",

    "operating_profit_margin_pct",

    "revenue_cagr_5yr",

    "pat_cagr_5yr",

    "debt_to_equity",

    "dividend_yield"

]

labels = [

    "ROE",

    "ROCE",

    "OPM",

    "Revenue CAGR",

    "PAT CAGR",

    "Debt/Equity",

    "Dividend Yield"

]

# ---------------------------------------------------------
# Peer Average
# ---------------------------------------------------------

peer_average = (
    peer_df[metrics]
    .mean()
)

selected_values = [
    company_data[m]
    for m in metrics
]

average_values = [
    peer_average[m]
    for m in metrics
]

# Close radar polygon

selected_values.append(selected_values[0])
average_values.append(average_values[0])

labels_closed = labels.copy()
labels_closed.append(labels[0])

# ---------------------------------------------------------
# Plotly Radar
# ---------------------------------------------------------

fig = go.Figure()

fig.add_trace(

    go.Scatterpolar(

        r=selected_values,

        theta=labels_closed,

        fill="toself",

        name=selected_company

    )

)

fig.add_trace(

    go.Scatterpolar(

        r=average_values,

        theta=labels_closed,

        fill="toself",

        name="Peer Average"

    )

)

fig.update_layout(

    polar=dict(
        radialaxis=dict(
            visible=True
        )
    ),

    showlegend=True,

    height=650,

    margin=dict(
        l=40,
        r=40,
        t=50,
        b=40
    )

)

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# KPI Summary
# =========================================================

section_header("KPI Summary")

peer_avg = peer_df[metrics].mean()

col1, col2, col3, col4 = st.columns(4)

# ---------------------------------------------------------
# ROE
# ---------------------------------------------------------

with col1:

    delta = round(
        company_data["return_on_equity_pct"] -
        peer_avg["return_on_equity_pct"],
        2
    )

    st.metric(

        label="ROE (%)",

        value=f'{company_data["return_on_equity_pct"]:.2f}%',

        delta=f"{delta:+.2f}%"

    )

# ---------------------------------------------------------
# ROCE
# ---------------------------------------------------------

with col2:

    delta = round(

        company_data["return_on_capital_employed_pct"] -

        peer_avg["return_on_capital_employed_pct"],

        2

    )

    st.metric(

        label="ROCE (%)",

        value=f'{company_data["return_on_capital_employed_pct"]:.2f}%',

        delta=f"{delta:+.2f}%"

    )

# ---------------------------------------------------------
# Revenue CAGR
# ---------------------------------------------------------

with col3:

    delta = round(

        company_data["revenue_cagr_5yr"] -

        peer_avg["revenue_cagr_5yr"],

        2

    )

    st.metric(

        label="Revenue CAGR",

        value=f'{company_data["revenue_cagr_5yr"]:.2f}%',

        delta=f"{delta:+.2f}%"

    )

# ---------------------------------------------------------
# PAT CAGR
# ---------------------------------------------------------

with col4:

    delta = round(

        company_data["pat_cagr_5yr"] -

        peer_avg["pat_cagr_5yr"],

        2

    )

    st.metric(

        label="PAT CAGR",

        value=f'{company_data["pat_cagr_5yr"]:.2f}%',

        delta=f"{delta:+.2f}%"

    )

# =========================================================
# Additional KPI Cards
# =========================================================

col5, col6, col7, col8 = st.columns(4)

with col5:

    st.metric(

        "OPM",

        f'{company_data["operating_profit_margin_pct"]:.2f}%'

    )

with col6:

    st.metric(

        "Debt / Equity",

        f'{company_data["debt_to_equity"]:.2f}'

    )

with col7:

    st.metric(

        "Dividend Yield",

        f'{company_data["dividend_yield"]:.2f}%'

    )

with col8:

    st.metric(

        "Market Cap",

        f'₹ {company_data["market_cap_crore"]:,.0f} Cr'

    )

# =========================================================
# Peer Comparison Table
# =========================================================

section_header("Peer Comparison Table")

display_df = peer_df[

    [

        "company_name",

        "market_cap_crore",

        "return_on_equity_pct",

        "return_on_capital_employed_pct",

        "operating_profit_margin_pct",

        "revenue_cagr_5yr",

        "pat_cagr_5yr",

        "debt_to_equity",

        "dividend_yield"

    ]

].copy()

display_df.columns = [

    "Company",

    "Market Cap (Cr)",

    "ROE",

    "ROCE",

    "OPM",

    "Revenue CAGR",

    "PAT CAGR",

    "Debt/Equity",

    "Dividend Yield"

]

# ---------------------------------------------------------
# Highlight Selected Company
# ---------------------------------------------------------

def highlight_company(row):

    if row["Company"] == selected_company:

        return [

            "background-color:#FFF3CD;font-weight:bold"

        ] * len(row)

    return [""] * len(row)

st.dataframe(

    display_df.style.apply(

        highlight_company,

        axis=1

    ),

    use_container_width=True,

    height=500

)

# =========================================================
# Download Results
# =========================================================

section_header("Export Data")

csv = display_df.to_csv(

    index=False

).encode("utf-8")

st.download_button(

    label="📥 Download Peer Comparison CSV",

    data=csv,

    file_name=f"{selected_group}_peer_comparison.csv",

    mime="text/csv"

)

# =========================================================
# Summary
# =========================================================

st.info(

    f"""
    **Peer Group:** {selected_group}

    **Companies Compared:** {len(display_df)}

    **Selected Company:** {selected_company}
    """

)

# =========================================================
# Footer
# =========================================================

st.divider()

st.caption(

    "N100 Financial Intelligence Platform | Peer Comparison Dashboard"

)

