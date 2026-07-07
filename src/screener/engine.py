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



