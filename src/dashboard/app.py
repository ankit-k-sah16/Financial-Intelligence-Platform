""""
DATABASE UTILITY FUNCTIONS
----------------------------------------------
Shared database access layer for the 
N100 Financial Intelligence Platform.

Every query is cached for 10 minutes.

"""

from pathlib import Path 
import sqlite3

import pandas as pd
import streamlit as st
from config.setting import DB_PATH

#---------------------------------------
# Connection
#---------------------------------------
@st.cache_resource
def get_connection():

    return sqlite3.connect(
        DB_PATH,check_same_thread=False)

#---------------------------------------
# Generic Query
#---------------------------------------
@st.cache_data(ttl=600)
def run_query(query,params=None):

    conn = get_connection()

    if params is None:
        params = ()

    return pd.read_sql_query(
        query,conn,params = params)

#---------------------------------------
# Companies
#---------------------------------------
@st.cache_data(ttl=600)
def get_companies():

    return run_query("""
        SELECT * 
        FROM stg_companies
        ORDER BY company_name
        """)

#---------------------------------------
# Ratios
#---------------------------------------
@st.cache_data(ttl=600)
def get_ratios(ticker,year=None):

    if year is None:
        query = """
        SELECT * FROM stg_financial_ratios 
        WHERE ticker=?
        ORDER BY year DESC
        """
        return run_query(query,(ticker,))

    query = """
    SELECT * FROM stg_financial_ratios
    WHERE ticker=?
      AND year=?
    """

    return run_query(query,(ticker, year))
        
        
    







