"""
================================================================================
Home Dashboard

N100 Financial Intelligence Platform

================================================================================

"""

from pathlib import Path
import sys
PROJECT_ROOT=Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_ROOT))

import streamlit as st
import pandas as pd 

from src.dashboard.utils.db import get_companies,get_all_ratios,get_sector_summary,get_market_cap_all,get_peer_groups

from src.dashboard.components.charts import create_kpi_card,create_bar_chart,create_donut_chart,create_horizontal_bar_chart,show

from src.dashboard.components.formatters import  format_market_cap,format_integer

from src.dashboard.components.theme import apply_theme,page_header,section_header

#==============================================================
# Theme
#==============================================================

apply_theme()

page_header(
    "Home Dashboard",
    "Overview of the N100 Financial Intelligence Platform"

)

#================================================================
# Load Data
#================================================================

companies = get_companies()

ratios = get_all_ratios()

sectors = get_sector_summary()

market_cap = get_market_cap_all()

peer_groups = get_peer_groups()

#================================================================
# Latest Financial Data
#================================================================

latest_ratios = (
    ratios.sort_values("year")
    .groupby("company_id").tail(1)
)

latest_market_cap = (
    market_cap.sort_values("year")
    .groupby("campany_id").tail(1)
)

#================================================================
# KPI Calculations
#================================================================

total_companies = latest_ratios["company_id"].nunique()

total_sectors = sectors['broad_sector'].nunique()

total_peer_groups = peer_groups['peer_group_name'].nunique()

total_market_cap = latest_market_cap['market_cap_crore'].sum()

# =====================================================
# KPI Cards
# =====================================================

section_header("Platform Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    create_kpi_card(
        "Companies",
        format_integer(total_companies)
    )

with col2:
    create_kpi_card(
        "Broad Sectors",
        format_integer(total_sectors)
    )

with col3:
    create_kpi_card(
        "Peer Groups",
        format_integer(total_peer_groups)
    )

with col4:
    create_kpi_card(
        "Total Market Cap",
        format_market_cap(total_market_cap)
    )

# =====================================================
# Sector Distribution
# =====================================================

st.markdown("")

section_header("Sector Distribution")

sector_counts = (
    latest_ratios
    .groupby("broad_sector")
    .size()
    .reset_index(name="Companies")
    .sort_values(
        "Companies",
        ascending=False
    )

)

col1, col2 = st.columns(2)

with col1:

    fig = create_bar_chart(
        sector_counts,
        x="broad_sector",
        y="Companies",
        title="Companies by Sector"
    )

    show(fig)

with col2:

    fig = create_donut_chart(
        sector_counts,
        names="broad_sector",
        values="Companies",
        title="Sector Share"
    )

    show(fig)

# =====================================================
# Market Cap Distribution
# =====================================================

section_header("Market Capitalisation")

market_summary = (
    latest_market_cap
    .merge(
        latest_ratios[
            [
                "company_id",
                "company_name",
                "broad_sector"
            ]
        ],
        on="company_id",
        how="left"
    )
)

market_summary = (
    market_summary
    .groupby(
        "broad_sector")
    ["market_cap_crore"]
    .sum().reset_index()
    .sort_values("market_cap_crore",
        ascending=False
    )
)

fig = create_bar_chart(
    market_summary,
    x="broad_sector",
    y="market_cap_crore",
    title="Market Cap by Sector"
)

show(fig)

# =====================================================
# Quick Statistics
# =====================================================

section_header("Quick Statistics")

left, right = st.columns(2)

with left:

    st.dataframe(
        sector_counts,
        use_container_width=True,
        hide_index=True
    )

with right:

    stats = pd.DataFrame({
        "Metric": [
            "Latest Financial Year",

            "Average ROE",

            "Average ROCE",

            "Average Debt/Equity",

            "Average Market Cap"
        ],

        "Value": [
            latest_ratios["year"].max(),

            round( latest_ratios["return_on_equity_pct"].mean(), 2 ),
    
            round( latest_ratios["return_on_capital_employed_pct"].mean(), 2  ),
          
            round(latest_ratios["debt_to_equity"].mean(), 2 ),
               
            format_market_cap(latest_market_cap["market_cap_crore"].mean())
        ]
    })

    st.dataframe( stats, use_container_width=True, hide_index=True )
       
# =====================================================
# Top 10 Companies by Market Cap
# =====================================================

section_header("Top 10 Companies by Market Capitalisation")

top_market_cap = (
    latest_market_cap
    .merge(
        latest_ratios[
            [   "company_id",
                "company_name",
                "market_cap"
            ]
        ],
        on="company_id",
        how="left"
    )
)

top_market_cap = (
    top_market_cap
    .sort_values(
        "market_cap_crore",
        ascending=False
    )
    .head(10)
)

fig = create_horizontal_bar_chart(
   
    top_market_cap,
    x="market_cap_crore",
    y="company_name",
    title="Top Companies by Market Cap"
)
show(fig)


# =====================================================
# Financial Health Distribution
# =====================================================

section_header("Financial Health")

col1, col2 = st.columns(2)

with col1:
    
    health = (
        latest_ratios
        .groupby("financial_health")
        .size()
        .reset_index(name="Companies")
    )

    fig = create_donut_chart(
        
        health,
        names="financial_health",
        values="Companies",
        title="Financial Health Distribution"
    )
    show(fig)

with col2:

    st.dataframe( health, use_container_width=True,hide_index=True )
  

# =====================================================
# Company Rating Distribution
# =====================================================

section_header("Company Ratings")

col1, col2 = st.columns(2)

with col1:

    rating = (
        latest_ratios
        .groupby("company_rating")
        .size()
        .reset_index(name="Companies")
        .sort_values(
            "company_rating"
        )
    )

    fig = create_bar_chart(
        rating,
        x="company_rating",
        y="Companies",
        title="Company Ratings"
    )
    show(fig)


with col2:

    st.dataframe(rating,use_container_width=True,hide_index=True )


# =====================================================
# Composite Quality Score
# =====================================================

section_header("Composite Quality Score")

top_quality = (

    latest_ratios
    .sort_values(
        "composite_quality_score",
        ascending=False
    ).head(10)
)

fig = create_horizontal_bar_chart(

    top_quality,
    x="composite_quality_score",
    y="company_name",
    title="Top 10 Quality Companies"
)
show(fig)

# =====================================================
# Top Companies Table
# =====================================================

section_header("Top Companies Snapshot")

snapshot = top_quality[
    [   "company_name",
        "broad_sector",
        "market_cap",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "debt_to_equity",
        "composite_quality_score",
        "company_rating",
        "financial_health"
    ]
].copy()

snapshot.columns = [

    "Company",
    "Sector",
    "Market Cap",
    "ROE (%)",
    "ROCE (%)",
    "D/E",
    "Quality Score",
    "Rating",
    "Health"
]

st.dataframe( snapshot, use_container_width=True, hide_index=True ) 
   
# =====================================================
# Platform Summary
# =====================================================

section_header("Platform Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"""
### Coverage

- Companies : {total_companies}
- Broad Sectors : {total_sectors}
- Peer Groups : {total_peer_groups}

""")

with col2:
    st.success(f"""
### Financials

Average ROE :
**{latest_ratios['return_on_equity_pct'].mean():.2f}%**

Average ROCE :
**{latest_ratios['return_on_capital_employed_pct'].mean():.2f}%**

""")


with col3:
    st.warning(f"""

### Market

Total Market Cap

**{format_market_cap(total_market_cap)}**

Latest FY

**{latest_ratios['year'].max()}**
""")


# =====================================================
# Database Statistics
# =====================================================

section_header("Database Statistics")

db_stats = pd.DataFrame({

    "Dataset":[ "Companies", "Financial Ratios", "Market Cap","Sectors" ],

    "Rows":[len(companies),len(ratios),len(market_cap), len(sectors)]
})

st.dataframe(db_stats,use_container_width=True,hide_index=True)

# =====================================================
# Footer
# =====================================================

st.divider()

st.caption("N100 Financial Intelligence Platform • Version 1.0")
    