""""
CAGR (Compound Annual Growth Rate) calculation for the N100 Financial Intelligence Platform.

"""

from math import pow

class CAGR_calculator:
    """"
    Compound Annual Growth Rate (CAGR) calculator class for financial analysis. 
     
    """
    #----------------------------------------------------------------
    #Generic CAGR 
    #----------------------------------------------------------------
    @staticmethod
    def calculate_cagr(start_value, end_value, years):
        """
        CAGR Formula:
         ((End Value / Start Value)^(1/Years)-1)*100

        Returns
        --------
        tuple (cagr_value, flag)

        """

        # Less than required years
        if years is None or years  <=0:
            return None ," Insufficiant data for CAGR calculation"
        
        # Missing Values
        if start_value is None or end_value is None:
            return None, "Missing values for CAGR calculation"
        
        # Zero Base 
        if start_value == 0:
            return None, "Zero base value for CAGR calculation"
        
        # Positive -> Negative
        if start_value > 0 and end_value < 0:
            return None, "DECLINE_TO_LOSS"
        
        # Negative -> Positive 
        if start_value < 0 and end_value > 0: 
            return None, "TURNAROUND"
        
        # Negative  -> Negative
        if start_value < 0 and end_value < 0:
            return None, "BOTH_NEGATIVE"
        
        # Positive -> Positive
        try:
            cagr= (pow(end_value/start_value,1/years)-1)*100

            return round(cagr,2), "CAGR_CALCULATED"

        except Exception:
            return None, "ERROR_IN_CAGR_CALCULATION"


     # -----------------------------
    # Revenue CAGR
    # -----------------------------

    @staticmethod
    def revenue_cagr(start_sales, end_sales,years):

        return CAGR_calculator.calculate_cagr(start_sales,
            end_sales,
            years
        )
    

    # -----------------------------
    # PAT CAGR
    # -----------------------------

    @staticmethod
    def pat_cagr(start_profit,end_profit,years):
        
        return CAGR_calculator.calculate_cagr(start_profit,          
            end_profit,
            years
        )


    # -----------------------------
    # EPS CAGR
    # -----------------------------

    @staticmethod
    def eps_cagr(start_eps, end_eps,years):
         
        return CAGR_calculator.calculate_cagr(start_eps,
            end_eps,
            years
        )


    # -----------------------------
    # Window helpers
    # -----------------------------

    @staticmethod
    def revenue_cagr_3yr(start_sales, end_sales):
        return CAGR_calculator.revenue_cagr(start_sales,
            end_sales,3)

    @staticmethod
    def revenue_cagr_5yr(start_sales, end_sales):
        return CAGR_calculator.revenue_cagr(start_sales, end_sales, 5)

    @staticmethod
    def revenue_cagr_10yr(start_sales, end_sales):
        return CAGR_calculator.revenue_cagr(start_sales, end_sales, 10)

    @staticmethod
    def pat_cagr_3yr(start_profit, end_profit):
        return CAGR_calculator.pat_cagr(start_profit, end_profit, 3)

    @staticmethod
    def pat_cagr_5yr(start_profit, end_profit):
        return CAGR_calculator.pat_cagr(start_profit, end_profit, 5)

    @staticmethod
    def pat_cagr_10yr(start_profit, end_profit):
        return CAGR_calculator.pat_cagr(start_profit, end_profit, 10)

    @staticmethod
    def eps_cagr_3yr(start_eps, end_eps):
        return CAGR_calculator.eps_cagr(start_eps, end_eps, 3)

    @staticmethod
    def eps_cagr_5yr(start_eps, end_eps):
        return CAGR_calculator.eps_cagr(start_eps, end_eps, 5)

    @staticmethod
    def eps_cagr_10yr(start_eps, end_eps):
        return CAGR_calculator.eps_cagr(start_eps, end_eps, 10)
                
        
        