""""
Ratio Engine

Computes financial KPIs from staging tables and stores results into stg_financial_ratios table.

"""
from pathlib import Path 
import sys
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
from config.setting import DB_PATH
from src.analytics.ratios import FinancialRatios
from src.analytics.cagr import CAGR_calculator
from src.analytics.cashflow import CashFlowAnalytics

class RatioEngine:
    """
    Financial KPI computation engine that computes financial ratios and stores them in the database.
    """
    def __init__(self):
        self.engine = create_engine(f"sqlite:///{DB_PATH}")

    #-------------------------------------------------------------
    # Loading Staging Tables
    #-------------------------------------------------------------
    def load_tables(self):

        self.pnl= pd.read_sql(
        "SELECT * FROM stg_profitandloss", self.engine
        )

        self.bs = pd.read_sql(
            "SELECT * FROM stg_balancesheet", self.engine 
        )

        self.cf = pd.read_sql(
            "SELECT * FROM stg_cashflow", self.engine 
        )

        self.company = pd.read_sql(
            "SELECT * FROM stg_companies",self.engine 
        )

        self.market_cap = pd.read_sql(
            "SELECT * FROM stg_market_cap", self.engine 
        )

        self.sectors = pd.read_sql(
            "SELECT * FROM stg_sectors", self.engine 
        )
        print("Loaded all Staging Tables")

    #-------------------------------------------------------------
    # Merging the Tables
    #-------------------------------------------------------------
    def merge_tables(self):

        df=self.pnl.merge(self.bs,on=["company_id","year"],how="left")

        df=df.merge(self.cf,on=["company_id","year"],how="left")

        df = df.drop(columns=["id_x", "id_y"], errors="ignore")
        
        df=df.merge(self.company,left_on="company_id",right_on="id")

        df=df.merge(self.sectors,on="company_id",how="left")
        df = df.drop(columns=["id_x", "id_y"], errors="ignore")
        df=df.merge(self.market_cap,on=["company_id","year"],how="left")

        self.df = df

        print(f"Merged Dataset shape:{self.df.shape}")

    #-------------------------------------------------------------
    # Sorting the Tables
    #-------------------------------------------------------------
    def prepare_dataframe(self):

        self.df=self.df.sort_values(
            by=["company_id","year"]).reset_index(drop=True
        )

        print("Data Sorted successfully")

    #-------------------------------------------------------------
    # Helper Funtion
    #-------------------------------------------------------------
    @staticmethod 
    def safe_float(value):
            
        try:

            if pd.isna(value):
                return None
            
            return float(value)
        
        except Exception:
            return None
        
    ## CAGR Helper
    def get_company_history(
                self, company_id):
            
        return self.df[
            self.df["company_id"]== company_id].sort_values("year")
        
    # -----------------------------------------------------
    # Company History
    # -----------------------------------------------------
    def get_company_history( self,company_id):
        """
        Returns complete financial history
        for one company ordered by year.
        """
        return (
            self.df[self.df["company_id"] == company_id].sort_values("year").reset_index(drop=True)
        )

    # -----------------------------------------------------
    # Previous Year Value
    # -----------------------------------------------------
    def get_previous_value( self, history, current_year, column, years_back):
        """
        Returns value exactly N years back.

        Example:
            current_year = 2024
            years_back = 5

            Returns value from 2019.
        """
        target_year = current_year - years_back

        previous = history[ history["year"] == target_year ]

        if previous.empty:
            return None
        
        return previous.iloc[0][column]

    #-------------------------------------------------------------
    # Computing Ratios
    #-------------------------------------------------------------
    def compute_ratios(self):
        """
        Computing financial ratios for each company-year.
        """
        results = []

        for _, row in self.df.iterrows():

            # --------------------------------------------------
            # Basic Fields
            # --------------------------------------------------
            company_id = row["company_id"]
            year = row["year"]

            sales = self.safe_float(row["sales"])
            operating_profit = self.safe_float(row["operating_profit"])
            other_income = self.safe_float(row["other_income"])
            interest = self.safe_float(row["interest"])
            net_profit = self.safe_float(row["net_profit"])
            eps = self.safe_float(row["eps"])
            dividend_payout = self.safe_float(row["dividend_payout"])

            equity = self.safe_float(row["equity_capital"])
            reserves = self.safe_float(row["reserves"])
            borrowings = self.safe_float(row["borrowings"])
            investments = self.safe_float(row["investments"])
            total_assets = self.safe_float(row["total_assets"])

            operating_activity = self.safe_float(row["operating_activity"])
            
            investing_activity = self.safe_float(row["investing_activity"])
            
            financing_activity = self.safe_float(row["financing_activity"])
            
            broad_sector = row.get("broad_sector",
                None)

            # --------------------------------------------------
            # Profitability Ratios
            # --------------------------------------------------
            net_profit_margin = (FinancialRatios.net_profit_margin(net_profit,
                    sales ))

            operating_profit_margin = (FinancialRatios.operating_profit_margin(operating_profit,
                    sales))
            
            roe = (FinancialRatios.return_on_equity( net_profit, equity,
                    reserves))
                
            # EBIT approximation
            ebit = None

            if ( operating_profit is not None and other_income is not None):
                ebit = (  operating_profit +other_income)

            roce = ( FinancialRatios.return_on_capital_employed(ebit,equity,reserves,
                    borrowings))

            roa = (FinancialRatios.return_on_assets(net_profit, total_assets))

            # --------------------------------------------------
            # ROCE Benchmark
            # --------------------------------------------------
            roce_check = ( FinancialRatios.roce_benchmark_check(roce,broad_sector
                ))

            roce_status = roce_check["status"]

            roce_type = roce_check.get("type", "percentage")

            roce_benchmark = roce_check["benchmark"]

            # --------------------------------------------------
            # Leverage Ratios
            # --------------------------------------------------
            debt_to_equity = (FinancialRatios.debt_to_equity(borrowings, equity,reserves))

            high_leverage_flag = (FinancialRatios.high_leverage_flag(debt_to_equity,broad_sector  ))
                

            interest_coverage = (FinancialRatios.interest_coverage_ratio(operating_profit,other_income,
                interest))

            icr_label = (FinancialRatios.icr_label(interest ))
            

            icr_warning = ( FinancialRatios.icr_warning_flag(interest_coverage))
            

            net_debt = ( FinancialRatios.net_debt(  borrowings,investments))
            
            # --------------------------------------------------
            # Efficiency Ratios
            # --------------------------------------------------
            asset_turnover = ( FinancialRatios.asset_turnover(sales,
                    total_assets ))            
            
            # --------------------------------------------------
            # Cash Flow KPIs
            # --------------------------------------------------

            free_cash_flow = (CashFlowAnalytics.free_cash_flow(operating_activity,
                    investing_activity))
            
            capex_value, capex_label = ( CashFlowAnalytics.capex_intensity(investing_activity,
                    sales))
            
            fcf_conversion = (CashFlowAnalytics.fcf_conversion_rate(free_cash_flow,
                    operating_profit))   

            capital_pattern = (CashFlowAnalytics.capital_allocation_pattern(operating_activity,investing_activity,
                    financing_activity))

            # --------------------------------------------------
            # Book Value Per Share
            # --------------------------------------------------
            book_value_per_share = None

            if ( equity is not None and reserves is not None ):
    
                face_value = self.safe_float(row.get("face_value", None))

                if (face_value is not None and face_value != 0 ):
                    book_value_per_share = round((equity + reserves)/ face_value,2)                  
                                        
            # --------------------------------------------------
            # Revenue CAGR
            # --------------------------------------------------
            history = self.get_company_history(company_id)
                
            sales_5yr = self.get_previous_value(history, year,"sales", 5)            
                            
            revenue_cagr_5yr = None
            revenue_cagr_flag = None

            if sales_5yr is not None:
                revenue_cagr_5yr, revenue_cagr_flag = (CAGR_calculator.revenue_cagr_5yr(sales_5yr,sales))

            else:
                revenue_cagr_flag = "INSUFFICIENT"
                        
            # --------------------------------------------------
            # PAT CAGR
            # --------------------------------------------------
            profit_5yr = self.get_previous_value(history,year,"net_profit",5)
                
            pat_cagr_5yr = None
            pat_cagr_flag = None

            if profit_5yr is not None:
                pat_cagr_5yr, pat_cagr_flag = (CAGR_calculator.pat_cagr_5yr( profit_5yr,net_profit ))   

            else:
                pat_cagr_flag = "INSUFFICIENT"

            # --------------------------------------------------
            # EPS CAGR
            # --------------------------------------------------
            eps_5yr = self.get_previous_value(history, year,"eps",5)   
            
            eps_cagr_5yr = None
            eps_cagr_flag = None

            if eps_5yr is not None:
                eps_cagr_5yr, eps_cagr_flag = (CAGR_calculator.eps_cagr_5yr
                    (eps_5yr,eps)
                )

            else:
                eps_cagr_flag = "INSUFFICIENT"

            # --------------------------------------------------
            # CFO Quality
            # --------------------------------------------------
            history5 = history[history["year"] <= year].tail(5)
            
            cfo_quality = None
            cfo_quality_label = None

            if len(history5) >= 5:
                cfo_quality, cfo_quality_label = (
                    CashFlowAnalytics.cfo_quality_score(history5["operating_activity"].tolist(),
                            history5["net_profit"].tolist()  ))
                    
            else:
                cfo_quality_label = "INSUFFICIENT"

            # --------------------------------------------------
            # Composite Quality Score
            # --------------------------------------------------
            composite_quality_score = (self.calculate_composite_score( roe,
                        roce,net_profit_margin, cfo_quality,
                        debt_to_equity, interest_coverage )                    
            )                          

            # --------------------------------------------------
            # Company Rating
            # --------------------------------------------------
            if composite_quality_score >= 80:
                company_rating = "Excellent"

            elif composite_quality_score >= 60:
                company_rating = "Good"

            elif composite_quality_score >= 40:
                company_rating = "Average"

            else:
                company_rating = "Weak"

            # --------------------------------------------------
            # Financial Health
            # --------------------------------------------------
            financial_health = "Healthy"

            if high_leverage_flag:
                financial_health = "High Leverage"

            if icr_warning:
                financial_health = "Debt Risk"

            if (high_leverage_flag and icr_warning):
                financial_health = "Financial Distress"

            # --------------------------------------------------
            # Save Result
            # --------------------------------------------------
            results.append({

                # --------------------------------------------------
                # Identity
                # --------------------------------------------------
                "company_id": company_id,
                "year": year,
                "company_name": row.get("company_name", None),
                "ticker": row.get("ticker", None),
                "broad_sector": broad_sector,

                # --------------------------------------------------
                # Raw Financial Data
                # --------------------------------------------------
                "sales": sales,
                "operating_profit": operating_profit,
                "other_income": other_income,
                "interest": interest,
                "net_profit": net_profit,
                "eps": eps,
                "equity": equity,
                "reserves": reserves,
                "borrowings": borrowings,
                "investments": investments,
                "total_assets": total_assets,
                "operating_activity": operating_activity,
                "investing_activity": investing_activity,
                "financing_activity": financing_activity,

                # --------------------------------------------------
                # Market Data
                # --------------------------------------------------
                "market_cap": self.safe_float(row.get("market_cap")),
                "pe": self.safe_float(row.get("pe")),
                "pb": self.safe_float(row.get("pb")),
                "dividend_yield": self.safe_float(row.get("dividend_yield")),

                # --------------------------------------------------
                # Profitability Ratios
                # --------------------------------------------------
                "net_profit_margin_pct": net_profit_margin,
                "operating_profit_margin_pct": operating_profit_margin,
                "return_on_equity_pct": roe,
                "return_on_capital_employed_pct": roce,
                "return_on_assets_pct": roa,

                # --------------------------------------------------
                # Leverage Ratios
                # --------------------------------------------------
                "debt_to_equity": debt_to_equity,
                "high_leverage_flag": high_leverage_flag,
                "interest_coverage": interest_coverage,
                "icr_label": icr_label,
                "icr_warning_flag": icr_warning,
                "net_debt": net_debt,

                # --------------------------------------------------
                # Efficiency
                # --------------------------------------------------
                "asset_turnover": asset_turnover,

                # --------------------------------------------------
                # Cash Flow
                # --------------------------------------------------
                "free_cash_flow_cr": free_cash_flow,
                "cash_from_operations_cr": operating_activity,
                "capex_cr": capex_value,
                "capex_label": capex_label,
                "fcf_conversion_rate": fcf_conversion,
                "capital_allocation_pattern": capital_pattern,

                # --------------------------------------------------
                # Shareholder Metrics
                # --------------------------------------------------
                "earnings_per_share": eps,
                "book_value_per_share": book_value_per_share,
                "dividend_payout_ratio_pct": dividend_payout,

                # --------------------------------------------------
                # Growth Metrics
                # --------------------------------------------------
                "revenue_cagr_5yr": revenue_cagr_5yr,
                "revenue_cagr_5yr_flag": revenue_cagr_flag,
                "pat_cagr_5yr": pat_cagr_5yr,
                "pat_cagr_5yr_flag": pat_cagr_flag,
                "eps_cagr_5yr": eps_cagr_5yr,
                "eps_cagr_5yr_flag": eps_cagr_flag,

                # Optional (if you compute these later)
                "revenue_cagr_3yr": row.get("revenue_cagr_3yr", None),
                "debt_declining": row.get("debt_declining", None),

                # --------------------------------------------------
                # Quality Metrics
                # --------------------------------------------------
                "cfo_quality_score": cfo_quality,
                "cfo_quality_label": cfo_quality_label,
                "roce_status": roce_status,
                "roce_type": roce_type,
                "roce_benchmark": roce_benchmark,

                # --------------------------------------------------
                # Overall Scores
                # --------------------------------------------------
                "composite_quality_score": composite_quality_score,
                "company_rating": company_rating,
                "financial_health": financial_health

            })      

        self.results = pd.DataFrame(results)

        print("=" * 80)
        print("NEW DATAFRAME COLUMNS")
        print(self.results.columns.tolist())
        print("=" * 80)

        self.results.sort_values(by=["company_id",
                    "year" ],inplace=True)

        self.results.reset_index(drop=True, inplace=True)  
        
        print()
        print("=" * 60)
        print("Ratio Calculation Completed")
        print(f"Rows Processed : {len(self.results)}")
        print("=" * 60)

        print()
        print("Computed KPI Columns")

        print(self.results.columns.tolist())
        print()
        print(self.results.head())
            

    # -----------------------------------------------------
    # Composite Quality Score
    # -----------------------------------------------------

    def calculate_composite_score( self,roe,roce, net_profit_margin,cfo_quality,debt_to_equity, interest_coverage):

        """
        Calculate Composite Quality Score (0–100).
        """

        score = 0

        # ROE (20)
        if roe is not None:

            if roe >= 20:
                score += 20

            elif roe >= 15:
                score += 15

            elif roe >= 10:
                score += 10

            else:
                score += 5

        # ROCE (20)
        if roce is not None:

            if roce >= 20:
                score += 20

            elif roce >= 15:
                score += 15

            elif roce >= 10:
                score += 10

            else:
                score += 5

        # Net Profit Margin (20)

        if net_profit_margin is not None:

            if net_profit_margin >= 20:
                score += 20

            elif net_profit_margin >= 10:
                score += 15

            elif net_profit_margin >= 5:
                score += 10

            else:
                score += 5

        # CFO Quality (20)

        if cfo_quality is not None:

            if cfo_quality >= 1:
                score += 20

            elif cfo_quality >= 0.75:
                score += 15

            elif cfo_quality >= 0.5:
                score += 10

            else:
                score += 5

        # Debt & ICR (20)

        leverage_score = 20

        if debt_to_equity is not None:

            if debt_to_equity > 5:
                leverage_score -= 10

            elif debt_to_equity > 2:
                leverage_score -= 5

        if interest_coverage is not None:

            if interest_coverage < 1.5:
                leverage_score -= 10

            elif interest_coverage < 3:
                leverage_score -= 5

        score += max(leverage_score, 0)

        return round(score, 2)

    # -----------------------------------------------------
    # Saving Results
    # -----------------------------------------------------
    def save_results(self):

        """
        Save calculated financial ratios
        into SQLite.
        """
        print()

        print("=" * 60)

        print("Saving Financial Ratios")

        print("=" * 60)

        self.results.to_sql("stg_financial_ratios",self.engine,if_exists="replace",
            index=False)
        
        print(f"{len(self.results)} rows written successfully.")
        pass

        # ---------------------------------------
        # Verifing Load
        # ---------------------------------------
        row_count = pd.read_sql(
            """
            SELECT COUNT(*) AS total
            FROM stg_financial_ratios
            """,self.engine
        ).iloc[0]["total"]

        print()

        print(f"Rows in stg_financial_ratios : {row_count}")  

        # ---------------------------------------
        # ETL Run Log
        # ---------------------------------------
        log = pd.DataFrame([{"pipeline_name":"Financial Ratio Engine",
            "status":"SUCCESS",
            "rows_processed":row_count,
            "execution_time":datetime.now()
        }])        
        log.to_sql( "etl_run_log",self.engine,if_exists="append", index=False) 

        print( "ETL Log Updated.")

        # ---------------------------------------
        # DQ Summary
        # ---------------------------------------
        dq = pd.DataFrame([{
            "dataset_name": "stg_financial_ratios",
            "total_rows":row_count,
            "failed_rows": 0,
            "success_rate": 100,
            "created_at":datetime.now()

        }])
        dq.to_sql( "dq_summary",self.engine, if_exists="append",index=False)

        print("DQ Summary Updated.")

        # ---------------------------------------
        # Manual Verification
        # ---------------------------------------
        sample = pd.read_sql(
            """
            SELECT company_id,year,return_on_equity_pct,
                revenue_cagr_5yr,composite_quality_score
            FROM stg_financial_ratios
            LIMIT 10    
            """,self.engine )
                
        print()
        print("Sample Output")  
        print(sample)

        print()
        print("=" * 60)
        print( "Financial Ratio Table Updated")
        print("=" * 60)

    #-------------------------------------------------------------
    # Running the Engine
    #-------------------------------------------------------------
   
    def run(self):

        print()
        print("=" * 60)
        print("Financial Ratio Engine Started")
        print("=" * 60)
        
        self.load_tables()
        self.merge_tables()
        self.prepare_dataframe()
        self.compute_ratios()
        self.save_results()

        print()
        print("=" * 60)
        print("Ratio Engine Completed Successfully")
        print("=" * 60)
    
        














































