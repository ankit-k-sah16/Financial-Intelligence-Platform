"""
N100 FINANCIAL INTELLIGENCE PLATFORM
MAIN STREAMLIT APPLICATION 

"""
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

import streamlit as st

#=====================================================
# Page Configuration
#=====================================================
st.set_page_config(
    page_title='Nifty100 Analytics',
    page_icon=':chart_with_upwards_trend:',
    layout="wide",
    initial_sidebar_state="expanded")

#=====================================================
# Session State
#=====================================================
if "selected_company"  not in st.session_state:
    st.session_state.selected_company = None

if "selected_year" not in st.session_state:
    st.session_state.selected_year = None

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

with st.sidebar:

    st.title(":chart_with_upwards_trend: N100 Analytics")

    st.markdown("---")

    st.success("Financial Intelligence Platform")

    st.markdown(
        """
            ### Navigation

            Use the pages below:

            🏠 Home

            🏢 Company Profile

            🔍 Screener

            👥 Peer Comparison

            📈 Financial Trends

            🏭 Sector Analytics

            💰 Capital Allocation

            📄 Reports
        """)
    st.markdown("-----")
    st.info("""
            Database
            SQLite
            92 Companies
            11 Peer Groups
            """
    )


# -------------------------------------------------------
# Main Page
# -------------------------------------------------------
st.title("📈 N100 Financial Intelligence Platform")

st.markdown(
"""
### Welcome

A professional financial analytics platform built for
the Nifty 100 universe.

This dashboard provides:

- Company Financial Analysis
- Intelligent Stock Screener
- Peer Group Comparison
- Sector Analytics
- Financial Trend Analysis
- Capital Allocation Analysis
- Interactive Reports
"""
)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Companies",
        "92"
    )

with col2:
    st.metric(
        "Peer Groups",
        "11"
    )

with col3:
    st.metric(
        "Financial Ratios",
        "40+"
    )

with col4:
    st.metric(
        "Dashboard",
        "Ready"
    )

st.markdown("---")

st.subheader("🚀 Getting Started")

st.write(
"""
Select any page from the left sidebar to begin exploring
the analytics platform.

Recommended order:

1. Company Profile
2. Screener
3. Peer Comparison
4. Financial Trends
5. Sector Analytics
6. Capital Allocation
7. Reports
"""
)

st.markdown("---")

st.caption(
    "Version 1.0 | N100 Financial Intelligence Platform"
)
