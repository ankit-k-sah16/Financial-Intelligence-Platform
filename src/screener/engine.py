""""
Stock Screener Engine
_______________________________________________________

Loads screener_config.yaml and applies configurable filters to the financial_ratios dataframe.

Features
----------------------------------------------------------
-> Supports all configurable screening metrics.
-> Financial Companies bypass D/E filter.
-> Debt Free companies always pass ICR filter.
-> Adds composite_quality_score.
-> Returns sorted DataFrame.

"""


from pathlib import Path
import numpy as np 
import pandas as pd
import yaml

#-----------------------------------------------------
# Financial Sectors
#-----------------------------------------------------
financial_sectors={
    "banks",
    "bank",
    "nbfc",
    "nbfcs",
    "insurance"
}

#-----------------------------------------------------
# Screener Engine
#-----------------------------------------------------
class ScreenerEngine:

    def __int__(self,config_path:str):
        
        self.config_path=Path(config_path)
        
        with open(self.config_path,"r",encoding="utf-8") as file:
            self.config=yaml.safe_load(file)

    #---------------------------------------------------

    @staticmethod
    def _is_financial(sector):
        
        if pd.isna(sector):
            return None

        return str(sector).strip().lower() in financial_sectors
    
    #------------------------------------------------------
    @staticmethod
    def _passes_icr(value,threshold):
        
        if threshold is None:
            return None
        
        if pd.isna(value):
            return None

        if isinstance(value,str): 
            if value.lower().strip() == "dabt free":
                return True
            
            try:
                value=float(value)
            
            except Exception:
                return False
        
        return value >= threshold
    
    #------------------------------------------------------

    def screen(self,ratios:pd.DataFrame):

        df=ratios.copy()

        filters=self.config.get("filters",{})

        # ROE
        #-------------------------
        value= filters.get("roe_min")

        if value is not None:
            df = df[df["roe"] >= value]


        # D/E
        #-------------------------
        value= filters.get("debt_to_equity_max")

        if value is not None:
            
            financial_mask=df['broad_sector'].apply(self._is_financial)

            non_financial=(~financial_mask) & (df['debt_to_equity'] >value)

            df=df[~non_financial]

        
        # FCF
        # -------------------------------------------------
        value = filters.get("fcf_min")

        if value is not None:
            df = df[df["free_cash_flow"] >= value]

        # -------------------------------------------------

        value = filters.get("revenue_cagr_5y_min")

        if value is not None:
            df = df[df["revenue_cagr_5y"] >= value]

        # -------------------------------------------------

        value = filters.get("pat_cagr_5y_min")

        if value is not None:
            df = df[df["pat_cagr_5y"] >= value]

        # -------------------------------------------------

        value = filters.get("opm_min")

        if value is not None:
            df = df[df["opm"] >= value]

        # -------------------------------------------------

        value = filters.get("pe_max")

        if value is not None:
            df = df[df["pe"] <= value]

        # -------------------------------------------------

        value = filters.get("pb_max")

        if value is not None:
            df = df[df["pb"] <= value]

        # -------------------------------------------------

        value = filters.get("dividend_yield_min")

        if value is not None:
            df = df[df["dividend_yield"] >= value]

        # ICR
        #-------------------------
        value= filters.get("interest_coverage_ratio_min")

        if value is not None:
            mask = df["interest_coverage"].apply(lambda x: self._passes_icr(x,value))

            df=df[mask]

        # -------------------------------------------------
        value = filters.get("market_cap_min")

        if value is not None:
            df = df[df["market_cap"] >= value]

        # -------------------------------------------------

        value = filters.get("net_profit_min")

        if value is not None:
            df = df[df["net_profit"] >= value]

        # -------------------------------------------------

        value = filters.get("eps_cagr_min")

        if value is not None:
            df = df[df["eps_cagr"] >= value]

        # -------------------------------------------------

        value = filters.get("asset_turnover_min")

        if value is not None:
            df = df[df["asset_turnover"] >= value]

        # -------------------------------------------------

        value = filters.get("sales_min")

        if value is not None:
            df = df[df["sales"] >= value]



        # --------------------------------------------------
        # Composite Quality Score
        # --------------------------------------------------

        score=(
            df['roe'].fillna(0)
            + df['roce'].fillna(0)
            + df['opm'].fillna(0)
            + df['revenue_cagr_5y'].fillna(0)
            + df['pat_cagr_5y'].fillna(0)
            + df['eps_cagr'].fillna(0)
            + (100 - df['debt_to_equity'].fillna(100)) 
        )

        df("composite_quality_score") = score

        df = df.sort_values(by="composite_quality_score",
            ascending=False).reset_index(drop=True)
        
        return df

            

            
        )
        

            


