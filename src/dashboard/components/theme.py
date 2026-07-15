""""
===========================================================================
Dashboard Theme
N100 Financial Intelligence Platform

Centralized styling for the Streamlit Dashboard.
===========================================================================
"""

import streamlit as st

#===========================================
# Color Palette
#===========================================
PRIMARY="#2563EB"
SECONDARY="#10B981"
SUCCESS="#22C55E"
DANGER="#DC2626"
WARNING="#F59E08"
INFO="#0EA5E9"
LIGHT="#F8FAFC"
DARK="#0F172A"
CARD="#FFFFFF"
TEXT="#1E293B"
BACKGROUND="#F8FAFC"
BORDER="#E2E8F0"

# =========================================================
# Chart Colors
# =========================================================

CHART_COLORS = [

    "#2563EB",

    "#10B981",

    "#F59E0B",

    "#DC2626",

    "#8B5CF6",

    "#06B6D4",

    "#84CC16",

    "#F97316",

    "#EC4899",

    "#64748B",

]

# =========================================================
# KPI Card Colors
# =========================================================

KPI_BLUE = "#2563EB"

KPI_GREEN = "#22C55E"

KPI_RED = "#EF4444"

KPI_ORANGE = "#F97316"

KPI_PURPLE = "#8B5CF6"

# =========================================================
# Status Colors
# =========================================================

STATUS = {

    "Excellent": "#16A34A",

    "Good": "#22C55E",

    "Average": "#FACC15",

    "Poor": "#EF4444",

    "Strong": "#22C55E",

    "Weak": "#EF4444",

}

#==============================================================
# Dashboard CSS
#==============================================================
def apply_theme():
    st.markdown(
        f"""

<style>

/* =================================================
Main App
================================================= */
.stApp {{
    background-color: {BACKGROUND};
}}


/* =================================================
Sidebar
================================================= */

[data-testid="stSidebar"] {{
    background-color:{DARK};
}}

[data-testid="stSidebar"] * {{
    color:white;
}}


/* =================================================
Metric Cards
================================================= */

[data-testid="metric-cantainer"] {{
    background:white;

    border:1px solid {BORDER};

    padding: 18px;

    border-radius:12px;

    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

/* =====================================================
Buttons
===================================================== */

.stButton>button {{

    border-radius:10px;

    border:none;

    background:{PRIMARY};

    color:white;

    padding:0.6rem 1.2rem;

    font-weight:600;

}}

.stButton>button:hover {{

    background:{SECONDARY};

}}


/* =====================================================
Download Button
===================================================== */

.stDownloadButton>button {{

    border-radius:10px;

    background:{SUCCESS};

    color:white;

}}


/* =====================================================
DataFrame
===================================================== */

[data-testid="stDataFrame"] {{

    border-radius:10px;

    border:1px solid {BORDER};

}}


/* =====================================================
Tabs
===================================================== */

button[data-baseweb="tab"] {{

    font-size:15px;

    font-weight:600;

}}


/* =====================================================
Headers
===================================================== */

h1{{
    color:{TEXT};
}}

h2{{
    color:{TEXT};
}}

h3{{
    color:{TEXT};
}}

h4{{
    color:{TEXT};
}}


/* =====================================================
Expander
===================================================== */

.streamlit-expanderHeader {{

    font-weight:bold;

}}


/* =====================================================
Alert Boxes
===================================================== */

.stAlert {{

    border-radius:10px;

}}


/* =====================================================
Divider
===================================================== */

hr {{

    margin-top:1rem;

    margin-bottom:1rem;

}}

</style>

""",

    unsafe_allow_html=True,

)

# =========================================================
# Page Header
# =========================================================

def page_header(

    title,

    subtitle=None,

):

    st.title(title)

    if subtitle:

        st.caption(subtitle)

    st.divider()

# =========================================================
# Section Header
# =========================================================

def section_header(title):

    st.subheader(title)

    st.divider()

# =========================================================
# Dashboard Footer
# =========================================================

def dashboard_footer():

    st.divider()

    st.caption(

        "© 2026 N100 Financial Intelligence Platform"

    )

# =========================================================
# Success
# =========================================================

def success(message):

    st.success(message)

# =========================================================
# Warning
# =========================================================

def warning(message):

    st.warning(message)

# =========================================================
# Error
# =========================================================

def error(message):

    st.error(message)

# =========================================================
# Info
# =========================================================

def info(message):

    st.info(message)

# =========================================================
# Empty State
# =========================================================

def empty(message="No data available."):

    st.info(message)

# =========================================================
# Color by Rating
# =========================================================

def rating_color(score):

    if score >= 80:

        return SUCCESS

    elif score >= 60:

        return INFO

    elif score >= 40:

        return WARNING

    return DANGER

# =========================================================
# Financial Health Color
# =========================================================

def health_color(label):

    label = str(label).lower()

    if label == "excellent":

        return SUCCESS

    elif label == "good":

        return SECONDARY

    elif label == "average":

        return WARNING

    return DANGER














