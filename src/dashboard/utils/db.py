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
            company_id,
            company_name,
            broad_sector
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