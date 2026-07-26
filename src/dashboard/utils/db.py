"""
=========================================================
Database Utility Functions
N100 Financial Intelligence Platform
=========================================================
"""

from pathlib import Path
import sys
import sqlite3

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(PROJECT_ROOT))

from config.setting import DB_PATH

# =========================================================
# Database Connection
# =========================================================
@st.cache_resource
def get_connection():
    """
    Returns a reusable SQLite connection.
    """

    return sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

# =========================================================
# Generic Query
# =========================================================
@st.cache_data(ttl=600)
def run_query(query, params=None):

    conn = get_connection()

    if params is None:
        params = ()

    return pd.read_sql_query(
        query,
        conn,
        params=params
    )

# =========================================================
# Companies
# =========================================================
@st.cache_data(ttl=600)
def get_companies():

    return run_query(
        """
        SELECT
            id AS company_id,
            company_name,
            company_logo,
            nse_profile,
            website,
            about_company
        FROM stg_companies
        ORDER BY company_name
        """
    )

# =========================================================
# Financial Ratios
# =========================================================

@st.cache_data(ttl=600)
def get_ratios(company_id, year=None):

    if year is None:

        return run_query(
            """
            SELECT *
            FROM stg_financial_ratios
            WHERE company_id=?
            ORDER BY year DESC
            """,
            (company_id,)
        )

    return run_query(
        """
        SELECT *
        FROM stg_financial_ratios
        WHERE company_id=?
        AND year=?
        """,
        (company_id, year)
    )

# =========================================================
# Profit & Loss
# =========================================================

@st.cache_data(ttl=600)
def get_pl(company_id):

    return run_query(
        """
        SELECT *
        FROM stg_profitandloss
        WHERE company_id=?
        ORDER BY year
        """,
        (company_id,)
    )

# =========================================================
# Balance Sheet
# =========================================================
@st.cache_data(ttl=600)
def get_bs(company_id):

    return run_query(
        """
        SELECT *
        FROM stg_balancesheet
        WHERE company_id=?
        ORDER BY year
        """,
        (company_id,)
    )

# =========================================================
# Cash Flow
# =========================================================
@st.cache_data(ttl=600)
def get_cf(company_id):

    return run_query(
        """
        SELECT *
        FROM stg_cashflow
        WHERE company_id=?
        ORDER BY year
        """,
        (company_id,)
    )

# =========================================================
# Sector List
# =========================================================
@st.cache_data(ttl=600)
def get_sectors():

    return run_query(
        """
        SELECT *
        FROM stg_sectors
        ORDER BY broad_sector
        """
    )

# =========================================================
# Peer Groups
# =========================================================
@st.cache_data(ttl=600)
def get_peer_groups():

    return run_query(
        """
        SELECT DISTINCT peer_group_name
        FROM stg_peer_groups
        ORDER BY peer_group_name
        """
    )

# =========================================================
# Peer Companies
# =========================================================
@st.cache_data(ttl=600)
def get_peers(group_name):

    return run_query(
        """
        SELECT *
        FROM peer_percentiles
        WHERE peer_group_name=?
        ORDER BY company_id
        """,
        (group_name,)
    )

# =========================================================
# Pros & Cons
# ========================================================= 
@st.cache_data(ttl=600)
def get_pros_cons(company_id):

    return run_query(
        """
        SELECT *
        FROM stg_prosandcons
        WHERE company_id=?
        """,
        (company_id,)
    )

# =========================================================
# Valuation 
# =========================================================
@st.cache_data(ttl=600)
def get_valuation(company_id):
    """
    Placeholder until valuation engine is implemented.
    """

    return pd.DataFrame()

@st.cache_data(ttl=600)
def get_all_ratios():
    return run_query("""
        SELECT *
        FROM stg_financial_ratios
    """)


@st.cache_data(ttl=600)
def get_market_cap_all():
    return run_query("""
        SELECT *
        FROM stg_market_cap
    """)


@st.cache_data(ttl=600)
def get_sector_summary():
    return run_query("""
        SELECT *
        FROM stg_sectors
    """)

# =========================================================
# Peer Comparison Data
# =========================================================

@st.cache_data(ttl=600)
def get_peer_comparison(group_name):

    return run_query(
        """
        SELECT

            pg.peer_group_name,

            c.company_id,

            c.company_name,

            c.broad_sector,

            c.sub_sector,

            fr.market_cap_crore,

            fr.return_on_equity_pct,

            fr.return_on_capital_employed_pct,

            fr.operating_profit_margin_pct,

            fr.revenue_cagr_5yr,

            fr.pat_cagr_5yr,

            fr.debt_to_equity,

            fr.dividend_yield

        FROM stg_peer_groups pg

        INNER JOIN stg_companies c

            ON pg.company_id = c.company_id

        INNER JOIN stg_financial_ratios fr

            ON pg.company_id = fr.company_id

        WHERE

            pg.peer_group_name = ?

        ORDER BY

            c.company_name

        """,

        (group_name,)

    )