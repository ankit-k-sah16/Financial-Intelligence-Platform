"""
=========================================================
Company Profile
N100 Financial Intelligence Platform
=========================================================
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_ROOT))

import streamlit as st
import pandas as pd

from src.dashboard.utils.db import get_peers




from src.dashboard.utils.db import (
    get_companies,
    get_company,
    get_ratios,
    get_market_cap
)

from src.dashboard.components.charts import (
    create_kpi_card,create_radar_chart
)

from src.dashboard.components.theme import (
    apply_theme,
    page_header,
    section_header,
    empty
)

from src.dashboard.components.formatters import (
    format_market_cap,
    format_percentage,
    format_ratio
)

# =========================================================
# Theme
# =========================================================

apply_theme()

page_header(
    "🏢 Company Profile",
    "Detailed Financial Analysis"
)

# =========================================================
# Load Companies
# =========================================================

companies = get_companies()

if companies.empty:

    empty("No companies available.")

    st.stop()

# =========================================================
# Sidebar Filters
# =========================================================

with st.sidebar:

    st.header("Filters")

    company_name = st.selectbox(

        "Select Company",

        companies["company_name"]

    )

# =========================================================
# Selected Company
# =========================================================

company_id = companies.loc[
    companies["company_name"] == company_name,
    "company_id"
].iloc[0]

company = get_company(company_id)

ratios = get_ratios(company_id)

market = get_market_cap(company_id)

if ratios.empty:

    empty("Financial ratios not available.")

    st.stop()

# =========================================================
# Financial Year
# =========================================================

years = sorted(

    ratios["year"].unique(),

    reverse=True

)

selected_year = st.selectbox(

    "Financial Year",

    years

)

ratio = ratios[
    ratios["year"] == selected_year
].iloc[0]

# =========================================================
# Company Information
# =========================================================

section_header("Company Overview")

left, right = st.columns([1, 3])

with left:

    logo = company.iloc[0]["company_logo"]

    if pd.notna(logo):

        st.image(

            logo,

            width=120

        )

with right:

    st.subheader(

        company.iloc[0]["company_name"]

    )

    st.write(

        company.iloc[0]["about_company"]

    )

    if pd.notna(company.iloc[0]["website"]):

        st.markdown(

            f"[🌐 Website]({company.iloc[0]['website']})"

        )

# =========================================================
# KPI Cards
# =========================================================

section_header("Key Financial Metrics")

market_cap = None

if not market.empty:

    latest_market = market.sort_values(

        "year"

    ).iloc[-1]

    market_cap = latest_market["market_cap_crore"]

col1, col2, col3 = st.columns(3)

with col1:

    create_kpi_card(

        "Market Cap",

        format_market_cap(market_cap)

        if market_cap is not None

        else "-"

    )

with col2:

    create_kpi_card(

        "ROE",

        format_percentage(

            ratio["return_on_equity_pct"]

        )

    )

with col3:

    create_kpi_card(

        "ROCE",

        format_percentage(

            ratio["return_on_capital_employed_pct"]

        )

    )

col4, col5, col6 = st.columns(3)

with col4:

    create_kpi_card(

        "P/E",

        format_ratio(

            ratio["pe"]

        )

    )

with col5:

    create_kpi_card(

        "P/B",

        format_ratio(

            ratio["pb"]

        )

    )

with col6:

    create_kpi_card(

        "Dividend Yield",

        format_percentage(

            ratio["dividend_yield"]

        )

    )

# =========================================================
# Business Summary
# =========================================================

section_header("Business Summary")

summary_left, summary_right = st.columns(2)

with summary_left:

    st.write("**Broad Sector**")

    st.success(

        ratio["broad_sector"]

    )

    st.write("**Company Rating**")

    st.info(

        ratio["company_rating"]

    )

with summary_right:

    st.write("**Financial Health**")

    st.success(

        ratio["financial_health"]

    )

    st.write("**Latest Financial Year**")

    st.info(

        selected_year

    )

# =========================================================
# Snapshot Table
# =========================================================

section_header("Current Year Snapshot")

snapshot = pd.DataFrame({

    "Metric":[

        "Revenue",

        "Operating Profit",

        "Net Profit",

        "EPS",

        "Debt / Equity",

        "Interest Coverage",

        "Asset Turnover",

        "Free Cash Flow"

    ],

    "Value":[

        ratio["sales"],

        ratio["operating_profit"],

        ratio["net_profit"],

        ratio["earnings_per_share"],

        ratio["debt_to_equity"],

        ratio["interest_coverage"],

        ratio["asset_turnover"],

        ratio["free_cash_flow_cr"]

    ]

})

st.dataframe(

    snapshot,

    use_container_width=True,

    hide_index=True

)

# =========================================================
# Financial Performance Trends
# =========================================================

from src.dashboard.utils.charts import (
    create_line_chart,
    create_multi_line_chart,
    show
)

section_header("Financial Performance Trends")

financial_trend = ratios.sort_values("year")

tab1, tab2 = st.tabs(
    [
        "Income Statement",
        "Profitability"
    ]
)

# =========================================================
# Income Statement
# =========================================================

with tab1:

    col1, col2 = st.columns(2)

    with col1:

        fig = create_line_chart(

            financial_trend,

            x="year",

            y="sales",

            title="Revenue Trend"

        )

        show(fig)

    with col2:

        fig = create_line_chart(

            financial_trend,

            x="year",

            y="operating_profit",

            title="Operating Profit Trend"

        )

        show(fig)

    st.markdown("")

    col3, col4 = st.columns(2)

    with col3:

        fig = create_line_chart(

            financial_trend,

            x="year",

            y="net_profit",

            title="Net Profit Trend"

        )

        show(fig)

    with col4:

        fig = create_line_chart(

            financial_trend,

            x="year",

            y="earnings_per_share",

            title="EPS Trend"

        )

        show(fig)


# =========================================================
# Profitability
# =========================================================

with tab2:

    fig = create_multi_line_chart(

        financial_trend,

        x="year",

        y_columns=[

            "return_on_equity_pct",

            "return_on_capital_employed_pct",

            "net_profit_margin_pct",

            "operating_profit_margin_pct"

        ],

        title="Profitability Trend"

    )

    show(fig)

# =========================================================
# Growth Trends
# =========================================================

section_header("Growth Analysis")

col1, col2 = st.columns(2)

with col1:

    fig = create_multi_line_chart(

        financial_trend,

        x="year",

        y_columns=[

            "revenue_cagr_5yr",

            "pat_cagr_5yr",

            "eps_cagr_5yr"

        ],

        title="Growth CAGR"

    )

    show(fig)

with col2:

    growth = financial_trend[

        [

            "year",

            "revenue_cagr_5yr",

            "pat_cagr_5yr",

            "eps_cagr_5yr"

        ]

    ]

    st.dataframe(

        growth,

        use_container_width=True,

        hide_index=True

    )

# =========================================================
# Margin Analysis
# =========================================================

section_header("Margin Analysis")

col1, col2 = st.columns(2)

with col1:

    fig = create_multi_line_chart(

        financial_trend,

        x="year",

        y_columns=[

            "net_profit_margin_pct",

            "operating_profit_margin_pct"

        ],

        title="Margin Trend"

    )

    show(fig)

with col2:

    margin_table = financial_trend[

        [

            "year",

            "net_profit_margin_pct",

            "operating_profit_margin_pct"

        ]

    ]

    margin_table.columns = [

        "Year",

        "Net Profit Margin",

        "Operating Margin"

    ]

    st.dataframe(

        margin_table,

        use_container_width=True,

        hide_index=True

    )

# =========================================================
# Profitability Summary
# =========================================================

section_header("Latest Profitability Snapshot")

summary = pd.DataFrame({

    "Metric":[

        "ROE",

        "ROCE",

        "ROA",

        "Net Profit Margin",

        "Operating Margin"

    ],

    "Latest Value":[

        ratio["return_on_equity_pct"],

        ratio["return_on_capital_employed_pct"],

        ratio["return_on_assets_pct"],

        ratio["net_profit_margin_pct"],

        ratio["operating_profit_margin_pct"]

    ]

})

st.dataframe(

    summary,

    use_container_width=True,

    hide_index=True

)

# =========================================================
# Balance Sheet Analysis
# =========================================================

from src.dashboard.utils.db import get_bs

section_header("Balance Sheet Analysis")

bs = get_bs(company_id)

if not bs.empty:

    bs = bs.sort_values("year")

    tab1, tab2 = st.tabs(
        [
            "Charts",
            "Snapshot"
        ]
    )

    with tab1:

        col1, col2 = st.columns(2)

        with col1:

            fig = create_multi_line_chart(

                bs,

                x="year",

                y_columns=[

                    "equity_share_capital",

                    "reserves"

                ],

                title="Equity & Reserves"

            )

            show(fig)

        with col2:

            fig = create_line_chart(

                bs,

                x="year",

                y="borrowings",

                title="Borrowings Trend"

            )

            show(fig)

    with tab2:

        bs_snapshot = bs.tail(1)[

            [

                "equity_share_capital",

                "reserves",

                "borrowings",

                "investments",

                "total_assets"

            ]

        ].T

        bs_snapshot.columns = ["Latest"]

        st.dataframe(

            bs_snapshot,

            use_container_width=True

        )

# =========================================================
# Cash Flow Analysis
# =========================================================

from src.dashboard.utils.db import get_cf

section_header("Cash Flow Analysis")

cf = get_cf(company_id)

if not cf.empty:

    cf = cf.sort_values("year")

    tab1, tab2 = st.tabs(
        [
            "Cash Flow Trends",
            "Cash Flow Breakdown"
        ]
    )

    # -----------------------------------------------------
    # Cash Flow Charts
    # -----------------------------------------------------

    with tab1:

        col1, col2 = st.columns(2)

        with col1:

            fig = create_multi_line_chart(

                cf,

                x="year",

                y_columns=[
                    "operating_activity",
                    "investing_activity",
                    "financing_activity"
                ],

                title="Cash Flow Components"

            )

            show(fig)

        with col2:

            fig = create_line_chart(

                ratios.sort_values("year"),

                x="year",

                y="free_cash_flow_cr",

                title="Free Cash Flow Trend"

            )

            show(fig)

    # -----------------------------------------------------
    # Cash Flow Table
    # -----------------------------------------------------

    with tab2:

        latest_cf = cf.tail(1)

        cash_table = latest_cf[

            [

                "operating_activity",

                "investing_activity",

                "financing_activity"

            ]

        ].T

        cash_table.columns = ["Latest"]

        st.dataframe(

            cash_table,

            use_container_width=True

        )

else:

    st.info("Cash Flow data not available.")

# =========================================================
# Capital Allocation Analysis
# =========================================================

section_header("Capital Allocation Analysis")

capital_df = ratios.sort_values("year")

tab1, tab2 = st.tabs(
    [
        "Capital Allocation",
        "Efficiency Metrics"
    ]
)

# ---------------------------------------------------------
# Capital Allocation Charts
# ---------------------------------------------------------

with tab1:

    col1, col2 = st.columns(2)

    with col1:

        fig = create_multi_line_chart(

            capital_df,

            x="year",

            y_columns=[
                "free_cash_flow_cr",
                "cash_from_operations_cr"
            ],

            title="Free Cash Flow vs CFO"

        )

        show(fig)

    with col2:

        fig = create_line_chart(

            capital_df,

            x="year",

            y="fcf_conversion_rate",

            title="FCF Conversion Rate"

        )

        show(fig)

# ---------------------------------------------------------
# Capital Allocation Metrics
# ---------------------------------------------------------

with tab2:

    latest = capital_df.iloc[-1]

    c1, c2 = st.columns(2)

    with c1:

        st.metric(

            "Capital Allocation Pattern",

            latest["capital_allocation_pattern"]

        )

        st.metric(

            "CFO Quality Score",

            round(

                latest["cfo_quality_score"],

                2

            )

        )

        st.metric(

            "CFO Quality Label",

            latest["cfo_quality_label"]

        )

    with c2:

        st.metric(

            "FCF Conversion",

            f"{latest['fcf_conversion_rate']:.2f}"

        )

        st.metric(

            "CapEx",

            f"₹{latest['capex_cr']:,.2f} Cr"

        )

        st.metric(

            "CapEx Label",

            latest["capex_label"]

        )

capital_table = capital_df[

    [

        "year",

        "free_cash_flow_cr",

        "cash_from_operations_cr",

        "fcf_conversion_rate",

        "capital_allocation_pattern",

        "cfo_quality_score",

        "cfo_quality_label",

        "capex_cr"

    ]

].copy()

capital_table.columns = [

    "Year",

    "Free Cash Flow",

    "Cash From Operations",

    "FCF Conversion",

    "Capital Allocation",

    "CFO Score",

    "CFO Label",

    "CapEx"

]

st.dataframe(

    capital_table,

    use_container_width=True,

    hide_index=True

)

# =========================================================
# Debt & Financial Strength
# =========================================================

section_header("Debt & Financial Strength")

debt_df = ratios.sort_values("year")

tab1, tab2 = st.tabs(
    [
        "Debt Trends",
        "Debt Metrics"
    ]
)

# ---------------------------------------------------------
# Debt Trend Charts
# ---------------------------------------------------------

with tab1:

    col1, col2 = st.columns(2)

    with col1:

        fig = create_multi_line_chart(

            debt_df,

            x="year",

            y_columns=[
                "borrowings",
                "net_debt"
            ],

            title="Borrowings vs Net Debt"

        )

        show(fig)

    with col2:

        fig = create_multi_line_chart(

            debt_df,

            x="year",

            y_columns=[
                "debt_to_equity",
                "interest_coverage"
            ],

            title="Debt/Equity & Interest Coverage"

        )

        show(fig)


# ---------------------------------------------------------
# Latest Financial Strength
# ---------------------------------------------------------

with tab2:

    latest = debt_df.iloc[-1]

    c1, c2, c3 = st.columns(3)

    with c1:

        create_kpi_card(

            "Debt / Equity",

            format_ratio(

                latest["debt_to_equity"]

            )

        )

    with c2:

        icr = latest["interest_coverage"]

        if isinstance(icr, str):

            create_kpi_card(

                "Interest Coverage",

                icr

            )

        else:

            create_kpi_card(

                "Interest Coverage",

                format_ratio(icr)

            )

    with c3:

        create_kpi_card(

            "Net Debt",

            format_market_cap(

                latest["net_debt"]

            )

        )

    st.markdown("")

# ---------------------------------------------------------
# Health Indicators
# ---------------------------------------------------------

left, right = st.columns(2)

with left:

    st.metric(

        "High Leverage Flag",

        latest["high_leverage_flag"]

    )

    st.metric(

        "ICR Warning",

        latest["icr_warning_flag"]

    )

with right:

    st.metric(

        "ICR Label",

        latest["icr_label"]

    )

    st.metric(

        "Debt Declining",

        latest["debt_declining"]

    )


# ---------------------------------------------------------
# Debt Analysis Table
# ---------------------------------------------------------

debt_table = debt_df[

    [

        "year",

        "borrowings",

        "net_debt",

        "debt_to_equity",

        "interest_coverage",

        "high_leverage_flag",

        "icr_label",

        "financial_health"

    ]

].copy()

debt_table.columns = [

    "Year",

    "Borrowings",

    "Net Debt",

    "Debt / Equity",

    "Interest Coverage",

    "High Leverage",

    "ICR Status",

    "Financial Health"

]

st.dataframe(

    debt_table,

    use_container_width=True,

    hide_index=True

)

# =========================================================
# Financial Statement Summary
# =========================================================

section_header("Financial Statement Summary")

latest_ratio = ratios.sort_values("year").iloc[-1]

summary = pd.DataFrame({

    "Financial Area": [

        "Revenue",
        "Operating Profit",
        "Net Profit",
        "Operating Cash Flow",
        "Free Cash Flow",
        "Borrowings",
        "Net Debt",
        "Market Capitalisation"

    ],

    "Latest Value": [

        latest_ratio["sales"],
        latest_ratio["operating_profit"],
        latest_ratio["net_profit"],
        latest_ratio["cash_from_operations_cr"],
        latest_ratio["free_cash_flow_cr"],
        latest_ratio["borrowings"],
        latest_ratio["net_debt"],
        latest_ratio["market_cap"]

    ]

})

st.dataframe(

    summary,

    use_container_width=True,

    hide_index=True

)

# =========================================================
# Financial Scorecard
# =========================================================

section_header("Financial Performance Scorecard")

c1, c2, c3, c4 = st.columns(4)

with c1:

    create_kpi_card(

        "Composite Score",

        f"{latest_ratio['composite_quality_score']:.1f}"

    )

with c2:

    create_kpi_card(

        "Company Rating",

        latest_ratio["company_rating"]

    )

with c3:

    create_kpi_card(

        "Financial Health",

        latest_ratio["financial_health"]

    )

with c4:

    create_kpi_card(

        "CFO Quality",

        latest_ratio["cfo_quality_label"]

    )

# =========================================================
# Key Financial Highlights
# =========================================================

section_header("Key Financial Highlights")

left, right = st.columns(2)

with left:

    st.success(f"""

### Growth

• Revenue CAGR (5Y): **{latest_ratio['revenue_cagr_5yr']:.2f}%**

• PAT CAGR (5Y): **{latest_ratio['pat_cagr_5yr']:.2f}%**

• EPS CAGR (5Y): **{latest_ratio['eps_cagr_5yr']:.2f}%**

""")

with right:

    st.info(f"""

### Profitability

• ROE: **{latest_ratio['return_on_equity_pct']:.2f}%**

• ROCE: **{latest_ratio['return_on_capital_employed_pct']:.2f}%**

• Net Margin: **{latest_ratio['net_profit_margin_pct']:.2f}%**

""")
    

# =========================================================
# Latest Financial Snapshot
# =========================================================

section_header("Latest Financial Snapshot")

snapshot = latest_ratio[

    [

        "sales",

        "operating_profit",

        "net_profit",

        "return_on_equity_pct",

        "return_on_capital_employed_pct",

        "debt_to_equity",

        "interest_coverage",

        "asset_turnover",

        "free_cash_flow_cr",

        "market_cap"

    ]

].to_frame()

snapshot.columns = ["Latest"]

st.dataframe(

    snapshot,

    use_container_width=True

)

# =========================================================
# Peer Comparison
# =========================================================

section_header("Peer Comparison")

peer_group = ratio["broad_sector"]

peer_df = get_peers(peer_group)

if peer_df.empty:

    st.warning(
        "No peer group available for this company."
    )

else:

    st.success(
        f"Peer Group : {peer_group}"
    )

    # -----------------------------------------------------
    # Company Rank
    # -----------------------------------------------------

    latest_year = peer_df["year"].max()

    peer_latest = peer_df[
        peer_df["year"] == latest_year
    ].copy()

    peer_latest = peer_latest.sort_values(

        "composite_quality_score",

        ascending=False

    ).reset_index(drop=True)

    peer_latest["Rank"] = (

        peer_latest.index + 1

    )

    company_rank = peer_latest.loc[

        peer_latest["company_id"] == company_id,

        "Rank"

    ]

    if not company_rank.empty:

        st.info(

            f"Peer Rank : {company_rank.iloc[0]} / {len(peer_latest)}"

        )

    # -----------------------------------------------------
    # Radar Chart
    # -----------------------------------------------------

    radar_metrics = [

        "return_on_equity_pct",

        "return_on_capital_employed_pct",

        "net_profit_margin_pct",

        "debt_to_equity",

        "free_cash_flow_cr",

        "pat_cagr_5yr",

        "revenue_cagr_5yr",

        "composite_quality_score"

    ]

    radar_labels = [

        "ROE",

        "ROCE",

        "NPM",

        "D/E",

        "FCF",

        "PAT CAGR",

        "Revenue CAGR",

        "Quality"

    ]

    company_values = []

    peer_values = []

    for metric in radar_metrics:

        company_values.append(

            latest_ratio.get(metric, 0)

        )

        peer_values.append(

            peer_latest[metric].mean()

        )

    fig = create_radar_chart(

        company_values,

        peer_values,

        radar_labels,

        title="Company vs Peer Average"

    )

    show(fig)

    # -----------------------------------------------------
    # Peer Summary
    # -----------------------------------------------------

    st.markdown("### Peer Summary")

    peer_summary = peer_latest[

        [

            "company_name",

            "composite_quality_score",

            "company_rating",

            "financial_health"

        ]

    ]

    st.dataframe(

        peer_summary,

        use_container_width=True,

        hide_index=True

    )

    # -----------------------------------------------------
    # Company vs Peer
    # -----------------------------------------------------

    comparison = pd.DataFrame({

        "Metric":[

            "ROE",

            "ROCE",

            "NPM",

            "PAT CAGR",

            "Revenue CAGR",

            "Quality Score"

        ],

        "Company":[

            latest_ratio["return_on_equity_pct"],

            latest_ratio["return_on_capital_employed_pct"],

            latest_ratio["net_profit_margin_pct"],

            latest_ratio["pat_cagr_5yr"],

            latest_ratio["revenue_cagr_5yr"],

            latest_ratio["composite_quality_score"]

        ],

        "Peer Average":[

            peer_latest["return_on_equity_pct"].mean(),

            peer_latest["return_on_capital_employed_pct"].mean(),

            peer_latest["net_profit_margin_pct"].mean(),

            peer_latest["pat_cagr_5yr"].mean(),

            peer_latest["revenue_cagr_5yr"].mean(),

            peer_latest["composite_quality_score"].mean()

        ]

    })

    st.dataframe(

        comparison,

        use_container_width=True,

        hide_index=True

    )