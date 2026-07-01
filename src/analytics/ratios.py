"""
Financial Ratios Calculation for the model
"""

class FinancialRatios:
   
    """
    Collection of reusable financial ratio claculations
    """

    @staticmethod
    def net_profit_margin(net_profit,sales):
        
        """
        Net Profit Margin(%) Formula: 
        
        (Net Profit/Sales)*100

        """

        try: 
            
            if sales in (0,None):
                return None
            
            return round((net_profit/sales)*100,2)
        
        except (TypeError, ZeroDivisionError):
            return None
        
    @staticmethod
    def  operating_profit_margin(operating_profit,sales):
      
        """
        Operating Profit Margin(%)

        Formula:
        (Operating Profit/Sales)*100

        Returns:
        float| None
        """

        try:

            if sales in(0,None):
                return None
            
            return round((operating_profit/sales)*100,2)
        
        except(TypeError,ZeroDivisionError):
            return None
        
    @staticmethod
    def return_on_equity(net_profit,equity_capital,reserves):
       
        """
        Return on Equity (ROE)

        Formula: ROE = Net Profit/(Equity Capital + Reserves)* 100

        """

        try:

            capital=equity_capital + reserves

            if capital<=0:
                return None
            
            return round((net_profit/capital)*100,2)
        
        except(TypeError,ZeroDivisionError):
            return None
        
    @staticmethod
    def return_on_capital_employed(ebit,equity_capital, reserves, borrowings ):

        """
        Return on Capital Employed (ROCE)

        Formula:
            EBIT /(Equity + Reserves + Borrowings)* 100
            
            
        """

        try:

            capital_employed = (equity_capital + reserves + borrowings)
                
            if capital_employed <= 0:
                return None

            return round( (ebit / capital_employed) * 100,2)
               
        except (TypeError, ZeroDivisionError):
            return None
        
    @staticmethod
    def return_on_assets(net_profit, total_assets):

        """
        Return on Assets (ROA)

        Formula: ROA = Net Profit/Total Assets * 100

        """

        try:

            if total_assets == 0:
                return None
            
            if total_assets is None:
                return None

            return round((net_profit / total_assets) * 100,2)
        
        except(TypeError,ZeroDivisionError):
            return None


    @staticmethod
    def roce_benchmark_check(roce ,broad_sector,sector_benchmark=12):
    
        """
        Validate ROCE.

        Financial companies use
        sector-relative benchmark.

        All other sectors use
        absolute threshold.
        
        """
        if roce is None:

            return {
                "status": "UNKNOWN",
                "benchmark": None
            }

        if broad_sector == "Financials":

            return {
                "status": ("PASS"                    
                    if roce >= sector_benchmark
                    else "FAIL"
                ),
                "benchmark": sector_benchmark,
                "type": "Sector Relative"
            }

        return { "status": ("PASS" 
                if roce >= 15
                else "FAIL"
            ),
            "benchmark": 15,
            "type": "Absolute"
        }
    
    
    @staticmethod
    def debt_to_equity(borrowings,equity_capital,reserves):
        
        """
        Debt to Equity Ratio (D/E)
        
        Formula: Borrowings/(Equity Capital + Reserves)
          Returns
        -------
        float | int | None

        Returns:
            0 if borrowings == 0
            None if equity + reserves <= 0
        
        """
        try:
            
            if borrowings==0 :
                return 0
            
            equity = equity_capital + reserves

            if equity <= 0:
                return None
            
            return round(borrowings/equity,2)
        
        except(TypeError,ZeroDivisionError):
            return None
        
        
    @staticmethod
    def high_leverage_flag(debt_to_equity, broad_sector):

        """
        High Leverage Flag

        Companies with High Leverages are flagged for further review.
        
        Companies outside the financial sector are flagged D/E when greater than 5. 
       
         """

        if debt_to_equity  is None :
            return False
        
        if broad_sector == "Financials":
            return False
        
        return debt_to_equity >5
    

    @staticmethod
    def interest_coverage_ratio(operating_profit, other_income,interest):

        """"
        Interest Coverage Ratio (ICR)
        
        Formula:(Operating Profit + Other Income)/ Interest
                  
        """
       
        try: 

            if interest == 0:
                return  None
            
            return round((operating_profit + other_income)/interest,2)
        
        except(TypeError,ZeroDivisionError):
            return None
    
    
    @staticmethod
    def icr_label(interest):
        
        """
        Display label for debt-free companies.
        
        """

        if interest == 0:
            return "Debt Free"
        
        return None


    @staticmethod
    def icr_warning_flag(interest_coverage_ratio):
        
        """
        Companies cannot comfortably service their debt if ICR is less than 1.5.
        
        """
        if interest_coverage_ratio is None:
            return False
        
        return interest_coverage_ratio < 1.5
    

    @staticmethod
    def net_debt(borrowings,investments):
        
        """
        Net Debt

        Formula:Borrowings - Investments
            
        """

        try:

            return round(borrowings - investments,2)
                
        except TypeError:

            return None


    @staticmethod
    def asset_turnover( sales,total_assets):
 
        """
        Asset Turnover Ratio

        Formula: Sales / Total Assets
  
        """

        try:

            if total_assets == 0:
                return None

            return round( sales / total_assets,2)
    
        except (TypeError, ZeroDivisionError):

            return None

        

            
        
        
        
        