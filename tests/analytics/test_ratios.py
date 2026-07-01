from pathlib import Path
import sys

PROJECT_ROOT=Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.analytics.ratios import FinancialRatios

#--------------------------------------------------------
# Net Profit Margin
#--------------------------------------------------------

def test_net_profit_margin_normal():
    assert(
        FinancialRatios.net_profit_margin(net_profit=250,sales=1000)==25.0
    )

def test_net_profit_margin_zero_sales():
    assert(
        FinancialRatios.net_profit_margin(net_profit=250,sales=0) is None
    )


#-----------------------------------------------------------
# Operating Profit Margin
#-----------------------------------------------------------

def test_operating_profit_margin_normal():
    assert(
        FinancialRatios.operating_profit_margin(operating_profit=300,sales=1200)==25.0
    )

def test_operating_profit_margin_zero_sales():
    assert(
        FinancialRatios.operating_profit_margin(operating_profit=300,sales=0) is None
    )


#--------------------------------------------------------------
# Return on Equity
#--------------------------------------------------------------

def test_return_on_equity_normal():
    
    assert(
        FinancialRatios.return_on_equity(net_profit=500,equity_capital=1000,reserves=1000)== 25.0   
    )

def test_return_on_equity_negative_equity():
    assert(
        FinancialRatios.return_on_equity(net_profit=500,equity_capital=-100,reserves=-200) is None       
    )


#--------------------------------------------------------------
# Return on Assets
#--------------------------------------------------------------

def test_return_on_assets_normal():
    assert(
        FinancialRatios.return_on_assets(net_profit=250,total_assets=1000) == 25.0     
    )

def test_return_on_assets_zero_assets():
    assert(
        FinancialRatios.return_on_assets(net_profit=250,total_assets=0) is None       
    )


# Debt-to-Equity
# ---------------------------------------------------

def test_debt_to_equity():

    assert (
        FinancialRatios.debt_to_equity(500,1000,1000 ) == 0.25
    )
            
def test_debt_free_returns_zero():

    assert (
        FinancialRatios.debt_to_equity(0, 1000,1000 ) == 0   
    )


# ---------------------------------------------------
# Interest Coverage Ratio
# ---------------------------------------------------

def test_interest_coverage():

    assert (
        FinancialRatios.interest_coverage_ratio( 400, 100,100 ) == 5.0
    )

def test_interest_zero_returns_none():

    assert (
        FinancialRatios.interest_coverage_ratio( 500,100,0 ) is None     
    )

# ---------------------------------------------------
# Debt Free Label
# ---------------------------------------------------

def test_icr_label():

    assert (
        FinancialRatios.icr_label(0) == "Debt Free"     
    )


# ---------------------------------------------------
# High Leverage
# ---------------------------------------------------

def test_high_leverage_flag():

    assert (
        FinancialRatios.high_leverage_flag( 6, "Industrials") is True
    )


# ---------------------------------------------------
# Net Debt
# ---------------------------------------------------

def test_net_debt():

    assert (
        FinancialRatios.net_debt(1000,300 ) == 700           
    )


# ---------------------------------------------------
# Asset Turnover
# ---------------------------------------------------

def test_asset_turnover():

    assert (
        FinancialRatios.asset_turnover( 1000,500) == 2.0
)    