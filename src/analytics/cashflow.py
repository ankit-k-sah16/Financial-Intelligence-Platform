""""
Cash Flow Analytics Module   
N100 Financial Intelligence Platform

"""


import pandas as pd 
class CashFlowAnalytics:

    #-------------------------
    # Free Cash Flow
    #-------------------------

    @staticmethod
    def free_cash_flow(operating_activity,investing_activity,):
        
        """
        FCF = CF0 + CFI
        
        Negative values are allowed.
        """
        try:
            return round(operating_activity + investing_activity,2)
        
        except TypeError:
            return None


    #-------------------------
    # CFO Quality Score
    #-------------------------  

    @staticmethod
    def cfo_quality_score(cfo_list,pat_list):
        """
        Average CFO/PAT over 5 years.
        
        """
        if len(cfo_list) < 5 or len(pat_list) < 5:
            return None, "INSUFFICIENT DATA: CFO and PAT lists must have at least 5 years of data."
        
        ratios=[]

        for cfo,pat in zip(cfo_list,pat_list):
            
            if pat == 0:
                return None , "PAT ZERO"
            
            ratios.append(cfo/pat)

        avg_ratio= sum (ratios)/ len(ratios)

        if avg_ratio > 1:
            label = "HIGH QUALITY"
        
        elif avg_ratio >= 0.5:
            label = "MEDIUM QUALITY"
        
        else:
            label = "LOW QUALITY/ ACCRUAL RISK "

        return round(avg_ratio,2),label
    

    #-------------------------
    # CapEx Intensity
    #------------------------- 

    @staticmethod
    def capex_intensity(investing_activity,sales):
        
        if sales == 0:
            return None, None
        
        capex=(abs(investing_activity)/sales)*100

        if capex < 3:
            label="Asset Light"

        elif capex <= 8:
            label="Moderate "

        else:
            label= "Capital Intensive"
        
        return round(capex,2),label
    

    #-------------------------
    # FCF Converstion
    #------------------------- 

    @staticmethod 
    def fcf_conversion_rate( free_cash_flow,operating_profit):
        
        if operating_profit == 0:
            return None
        
        return round((free_cash_flow/operating_profit)*100,2)
    

     # -------------------------------------------------
    # Capital Allocation Pattern
    # -------------------------------------------------

    @staticmethod
    def capital_allocation_pattern(cfo,cfi,cff,cfo_pat_ratio=None):

        signs = (
            "+" if cfo >= 0 else "-",
            "+" if cfi >= 0 else "-",
            "+" if cff >= 0 else "-"
        )

        if signs == ("+", "-", "-"):

            if (cfo_pat_ratio is not None and cfo_pat_ratio > 1 ):
                
                 return "Shareholder Returns"

               
            return "Reinvestor"

        elif signs == ("+", "+", "-"):

            return "Liquidating Assets"

        elif signs == ("-", "+", "+"):

            return "Distress Signal"

        elif signs == ("-", "-", "+"):

            return "Growth Funded by Debt"

        elif signs == ("+", "+", "+"):

            return "Cash Accumulator"

        elif signs == ("-", "-", "-"):

            return "Pre-Revenue"

        elif signs == ("+", "-", "+"):

            return "Mixed"

        return "Unknown"

    # -------------------------------------------------
    # Capital Allocation Report
    # -------------------------------------------------

    @staticmethod
    def generate_capital_allocation_report( df, output_file):
       
        rows = []

        for _, row in df.iterrows():

            pattern = ( CashFlowAnalytics .capital_allocation_pattern(
                    row["operating_activity"],
                    row["investing_activity"],
                    row["financing_activity"]
                )
            )  
   
            rows.append({

                "company_id": row["company_id"],
                   
                "year":row["year"],
                    
                "cfo_sign":"+" if row["operating_activity"] >= 0 else "-",
                    
                "cfi_sign":"+" if row["investing_activity"] >= 0 else "-",
                    
                "cff_sign":"+" if row["financing_activity"] >= 0 else "-",
                    
                "pattern_label": pattern

            })

        report = pd.DataFrame(rows)

        report.to_csv( output_file, index=False)
           
        return report