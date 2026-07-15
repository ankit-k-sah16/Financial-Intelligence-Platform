""""
==========================================================================
Formatting Utilities
N100 Financial Intelligence Platform

Reusable formatting functions for  Streamlit Dashboard
===========================================================================

"""

import math 
import pandas as pd

#========================================
# Missing Values
#========================================
def format_na(value,default='-'):

    if value is None:
        return default
    
    if pd.isna(value):
        return default
    
    return value

#========================================
# Percentage
#========================================
def format_percentage(value,decimals=2):

    if pd.isna(value):
        return "-"
    
    return (f"{value:.{decimals}f}%")

#========================================
# Ratios
#========================================
def foramt_ratios(value,decimals=2):

    if pd.isna(value):
        return "-"
    
    return (f"{value:.{decimals}f}%")

#========================================
# Currency
#========================================
def foramt_currency(value, decimals=2):
    
    if pd.isna(value):
        return "-"
    
    return (f"{value:,.{decimals}f}%")

# =========================================================
# Crores
# =========================================================

def format_crore(value):

    if pd.isna(value):
        return "-"

    return f"₹{value:,.2f} Cr"

# =========================================================
# Lakhs
# =========================================================
def format_lakh(value):

    if pd.isna(value):
        return "-"

    return f"₹{value:,.2f} L"

# =========================================================
# Market Cap
# =========================================================
def format_market_cap(value):
    """
    Formats values in Crore.
    """

    if pd.isna(value):
        return "-"

    if value >= 100000:

        return f"₹{value/100000:.2f} L Cr"

    return f"₹{value:,.2f} Cr"

# =========================================================
# Large Numbers
# =========================================================
def format_large_number(value):

    if pd.isna(value):
        return "-"

    value = float(value)

    if value >= 1_000_000_000:

        return f"{value/1_000_000_000:.2f} B"

    if value >= 1_000_000:

        return f"{value/1_000_000:.2f} M"

    if value >= 1_000:

        return f"{value/1_000:.2f} K"

    return f"{value:.2f}"

# =========================================================
# Integer
# =========================================================
def format_integer(value):

    if pd.isna(value):
        return "-"

    return f"{int(value):,}"

# =========================================================
# Date
# =========================================================
def format_date(value):

    if pd.isna(value):
        return "-"

    return pd.to_datetime(value).strftime("%d-%b-%Y")

# =========================================================
# Financial Health
# =========================================================
def format_financial_health(label):

    if pd.isna(label):
        return "-"

    return str(label).title()

# =========================================================
# Company Rating
# =========================================================
def format_rating(rating):

    if pd.isna(rating):
        return "-"

    return f"⭐ {rating}"

# =========================================================
# Boolean
# =========================================================
def format_boolean(value):

    if value:

        return "Yes"

    return "No"

# =========================================================
# CAGR
# =========================================================
def format_cagr(value):

    if pd.isna(value):
        return "-"

    return f"{value:.2f}% CAGR"

# =========================================================
# Growth
# =========================================================
def growth_arrow(value):

    if pd.isna(value):
        return "-"

    if value > 0:

        return f"▲ {value:.2f}%"

    elif value < 0:

        return f"▼ {abs(value):.2f}%"

    return "0%"

# =========================================================
# Debt/Equity
# =========================================================
def format_de(value):

    if pd.isna(value):
        return "-"

    return f"{value:.2f}x"


# =========================================================
# Interest Coverage
# =========================================================
def format_icr(value):

    if isinstance(value, str):

        return value

    if pd.isna(value):

        return "-"

    return f"{value:.2f}x"


# =========================================================
# Score
# =========================================================
def format_score(value):

    if pd.isna(value):

        return "-"

    return f"{value:.1f}/100"


# =========================================================
# Company Name
# =========================================================
def format_company(name):

    if pd.isna(name):

        return "-"

    return str(name).title()


# =========================================================
# Sector
# =========================================================
def format_sector(name):

    if pd.isna(name):

        return "-"

    return str(name).title()


# =========================================================
# Capital Allocation
# =========================================================
def format_capital_pattern(value):

    if pd.isna(value):

        return "-"

    return str(value).replace("_", " ").title()


# =========================================================
# Generic Formatter
# =========================================================
def auto_format(column, value):
    """
    Automatically format a value
    based on its column name.
    """

    column = column.lower()

    if "percentage" in column:

        return format_percentage(value)

    if "margin" in column:

        return format_percentage(value)

    if "cagr" in column:

        return format_percentage(value)

    if "market_cap" in column:

        return format_market_cap(value)

    if "score" in column:

        return format_score(value)

    if "debt_to_equity" in column:

        return format_de(value)

    if "interest_coverage" in column:

        return format_icr(value)

    if "company_rating" in column:

        return format_rating(value)

    if "financial_health" in column:

        return format_financial_health(value)

    return format_na(value)