"""
STOCK SCREENER PRESETS

Predefined investment strategies for the N100 Financial Intelligence Platform

"""

PRESETS={
    "quality_compounder": {
        "roe_min": 15,
        "debt_to_equity_max": 1.0,
        "fcf_min": 0,
        "revenue_cagr_5yr_min": 10,
    },

    "value_pick": {

        "pe_max": 20,
        "pb_min": 3.0,
        "debt_to_equity": 2.0,
        "dividend_yield_min": 1.0,
    },

    "growth_accelerator": {
        "pat_cagr_5yr_min" :20,
        "revenue_cagr_5yr_min": 15,
        "debt_to_equity_max": 2.0,
    },
    
    "dividend_champion": {

        "dividend_yield_min": 2,
        "dividend_payout_max": 80,
        "fcf_min": 0,
    },

    "debt_free_blue_chip": {

        "debt_to_equity_max": 0,
        "roe_min": 12,
        "sales_min": 5000,
    },

    "turnaround_watch": {

        "revenue_cagr_3yr_min": 10,
        "fcf_latest_positive": True,
        "debt_declining": True,
    }

}