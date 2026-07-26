"""
=========================================================
Annual Reports
N100 Financial Intelligence Platform
=========================================================
"""

# =========================================================
# Imports
# =========================================================

import streamlit as st
import pandas as pd

from components.theme import (
    apply_theme,
    page_header,
    section_header
)

from utils.db import (
    get_companies,
    get_reports
)

# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(

    page_title="Annual Reports",

    page_icon="📄",

    layout="wide"

)

apply_theme()

page_header(

    "📄 Annual Reports",

    "Browse and download company annual reports."

)

# =========================================================
# Load Data
# =========================================================

companies_df = get_companies()

reports_df = get_reports()

# =========================================================
# Validate Data
# =========================================================

if companies_df.empty:

    st.error(

        "Company master data not found."

    )

    st.stop()

if reports_df.empty:

    st.warning(

        "No annual reports available."

    )

    st.stop()

# =========================================================
# Merge Company Information
# =========================================================

reports_df = reports_df.merge(

    companies_df[

        [

            "company_id",

            "company_name",

            "broad_sector"

        ]

    ],

    on="company_id",

    how="left"

)

reports_df = reports_df.sort_values(

    [

        "company_name",

        "year"

    ],

    ascending=[

        True,

        False

    ]

)

reports_df.reset_index(

    drop=True,

    inplace=True

)

# =========================================================
# Annual Report Overview
# =========================================================

section_header("Annual Report Overview")

# ---------------------------------------------------------
# Calculate KPIs
# ---------------------------------------------------------

total_reports = len(reports_df)

total_companies = reports_df["company_id"].nunique()

latest_year = reports_df["year"].max()

oldest_year = reports_df["year"].min()

avg_reports = round(

    total_reports /

    total_companies,

    1

)

available_sectors = reports_df[

    "broad_sector"

].nunique()

# =========================================================
# KPI Cards - Row 1
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(

        "Total Reports",

        f"{total_reports:,}"

    )

with col2:

    st.metric(

        "Companies Covered",

        f"{total_companies:,}"

    )

with col3:

    st.metric(

        "Latest Financial Year",

        latest_year

    )

# =========================================================
# KPI Cards - Row 2
# =========================================================

col4, col5, col6 = st.columns(3)

with col4:

    st.metric(

        "Oldest Financial Year",

        oldest_year

    )

with col5:

    st.metric(

        "Avg Reports / Company",

        avg_reports

    )

with col6:

    st.metric(

        "Sectors Covered",

        available_sectors

    )


# =========================================================
# Company Search
# =========================================================

section_header("Search Annual Reports")

company_list = (

    reports_df

    [

        "company_name"

    ]

    .dropna()

    .sort_values()

    .unique()

    .tolist()

)

selected_company = st.selectbox(

    "Select Company",

    company_list

)

# =========================================================
# Filter Company Reports
# =========================================================

company_reports = (

    reports_df

    [

        reports_df["company_name"]

        ==

        selected_company

    ]

    .copy()

)

company_reports = company_reports.sort_values(

    "year",

    ascending=False

)

# =========================================================
# Company Information
# =========================================================

sector = company_reports.iloc[0]["broad_sector"]

st.info(

    f"""

    **Company:** {selected_company}

    **Sector:** {sector}

    **Reports Available:** {len(company_reports)}

    """

)

# =========================================================
# Available Years
# =========================================================

section_header("Available Report Years")

years = (

    company_reports

    [

        "year"

    ]

    .tolist()

)

selected_year = st.selectbox(

    "Select Financial Year",

    years

)

selected_report = (

    company_reports

    [

        company_reports["year"]

        ==

        selected_year

    ]

    .iloc[0]

)

# =========================================================
# Report Details
# =========================================================

section_header("Annual Report Details")

report_name = selected_report.get(

    "document_name",

    "Annual Report"

)

report_url = selected_report.get(

    "document_url",

    None

)

document_type = selected_report.get(

    "document_type",

    "Annual Report"

)

# =========================================================
# Report Information
# =========================================================

col1, col2 = st.columns([2, 1])

with col1:

    st.write("### Report Information")

    st.write(

        f"**Company:** {selected_company}"

    )

    st.write(

        f"**Financial Year:** {selected_year}"

    )

    st.write(

        f"**Document Type:** {document_type}"

    )

    st.write(

        f"**Document Name:** {report_name}"

    )

with col2:

    st.write("### Availability")

    if pd.notna(report_url) and str(report_url).strip() != "":

        st.success("✅ Report Available")

    else:

        st.error("❌ Report Unavailable")

# =========================================================
# PDF Access
# =========================================================

section_header("Open Annual Report")

if pd.notna(report_url) and str(report_url).strip() != "":

    st.link_button(

        "📄 Open Annual Report (BSE PDF)",

        report_url,

        use_container_width=True

    )

else:

    st.error(

        "Annual report is not available for the selected financial year."

    )

# =========================================================
# Report History
# =========================================================

section_header("Report History")

history_df = company_reports.copy()

history_df["Status"] = history_df["document_url"].apply(

    lambda x: "✅ Available"

    if pd.notna(x) and str(x).strip() != ""

    else "❌ Unavailable"

)

display_history = history_df[

    [

        "year",

        "document_type",

        "document_name",

        "Status"

    ]

].rename(

    columns={

        "year":"Financial Year",

        "document_type":"Type",

        "document_name":"Document"

    }

)

st.dataframe(

    display_history,

    use_container_width=True,

    hide_index=True

)

# =========================================================
# Download / Open Report
# =========================================================

section_header("Document Access")

if pd.notna(report_url) and str(report_url).strip() != "":

    col1, col2 = st.columns(2)

    with col1:

        st.link_button(

            "📄 Open BSE Report",

            report_url,

            use_container_width=True

        )

    with col2:

        st.success(

            "Report available."

        )

else:

    st.error(

        "Annual report unavailable."

    )

# =========================================================
# Copy URL
# =========================================================

if pd.notna(report_url) and str(report_url).strip() != "":

    st.code(

        report_url,

        language="text"

    )

# =========================================================
# Footer Summary
# =========================================================

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:

    st.info(

        f"""

        **Company**

        {selected_company}

        """

    )

with col2:

    st.info(

        f"""

        **Financial Year**

        {selected_year}

        """

    )

with col3:

    availability = (

        "Available"

        if pd.notna(report_url)

        and str(report_url).strip() != ""

        else "Unavailable"

    )

    st.info(

        f"""

        **Report Status**

        {availability}

        """

    )

st.caption(

    "N100 Financial Intelligence Platform • Annual Reports Dashboard"
)

