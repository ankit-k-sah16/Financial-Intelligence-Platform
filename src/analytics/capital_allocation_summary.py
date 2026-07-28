"""
Capital Allocation Summary Engine
---------------------------------

Sprint 3
N100 Financial Intelligence Platform

Responsibilities
----------------
1. Verify capital_allocation.csv completeness
2. Generate allocation distribution
3. Merge allocation with cashflow intelligence
4. Generate pattern changes report
"""

from pathlib import Path
import logging

import pandas as pd

logger = logging.getLogger(__name__)

class CapitalAllocationSummary:
    """
    Capital Allocation Summary Engine.
    """

    def __init__(self,allocation_file,cashflow_file, output_dir):
        """
        Parameters
        ----------
        allocation_file : Path
            capital_allocation.csv

        cashflow_file : Path
            cashflow_intelligence.xlsx

        output_dir : Path
            Output folder
        """

        self.output_dir = Path(output_dir)

        self.allocation = pd.read_csv(allocation_file)

        self.cashflow = pd.read_excel(cashflow_file)

        # -----------------------------
        # Standardize column names
        # -----------------------------
        self.allocation.columns = (self.allocation.columns.str.strip().str.lower())
    
        # Standardize column names
        self.allocation.rename(columns={"pattern_label":"capital_allocation_label"},inplace=True)

        self.cashflow.columns = (self.cashflow.columns.str.strip().str.lower())
        for df in [self.cashflow, self.allocation]:
                df["company_id"] = (df["company_id"].astype(str).str.strip().str.upper())

        logger.info("Capital Allocation Summary initialized.")

    def _verify_completeness(self):
        """
        Verify capital allocation dataset.

        Checks
        ------
        1. Duplicate records
        2. Missing allocation labels
        3. Missing years
        4. Missing companies
        """

        logger.info("Verifying capital allocation dataset...")

        # ---------------------------------
        # Duplicate rows
        # ---------------------------------
        duplicates = self.allocation.duplicated(subset=["company_id", "year"]
        ).sum()

        if duplicates > 0:
            logger.warning(f"Duplicate rows found: {duplicates}")

        else:
            logger.info("No duplicate company-year records.")

        # ---------------------------------
        # Missing allocation
        # ---------------------------------
        missing_alloc = (
            self.allocation[ "capital_allocation_label"
            ].isna().sum())
   
        if missing_alloc > 0:
            logger.warning(f"Missing allocation labels: {missing_alloc}")
            
        else:
            logger.info("No missing allocation labels.")
        
        # ---------------------------------
        # Company Count
        # ---------------------------------

        company_count = (self.allocation["company_id"
            ].nunique() )
    
        logger.info(f"Unique companies: {company_count}")
        

        if company_count != 92:
            logger.warning(f"Expected 92 companies but found {company_count}")
       
        # ---------------------------------
        # Year Coverage
        # ---------------------------------
        years_per_company = (self.allocation
            .groupby("company_id")["year"] .nunique() )
           
        expected_years = ( self.allocation["year"] .nunique())
         
        incomplete = years_per_company[ years_per_company != expected_years]

        if not incomplete.empty:

            logger.warning(f"{len(incomplete)} companies have incomplete year coverage." )

            incomplete.reset_index( name="available_years"
                ).to_csv(self.output_dir /
                "allocation_missing_years.csv",
                index=False,
            )  

        else:
            logger.info("All companies have complete year coverage." )
                
        # ---------------------------------
        # Verification Summary
        # ---------------------------------
        verification = pd.DataFrame(
            [
                {
                    "metric": "unique_companies",
                    "value": company_count,
                },
                {
                    "metric": "expected_companies",
                    "value": 92,
                },
                {
                    "metric": "unique_years",
                    "value": expected_years,
                },
                {
                    "metric": "duplicate_records",
                    "value": duplicates,
                },
                {
                    "metric": "missing_allocations",
                    "value": missing_alloc,
                },
                {
                    "metric": "companies_with_missing_years",
                    "value": len(incomplete),
                },
            ]
        )

        verification.to_csv(self.output_dir /
            "capital_allocation_verification.csv", index=False,)

        logger.info("Verification complete.")
      
        return verification
    def _generate_distribution(self):
        """
        Generate capital allocation distribution using the
        latest available record for each company.

        Output
        ------
        capital_allocation_distribution.csv
        """

        logger.info( "Generating capital allocation distribution...")
   
        # --------------------------------------------------
        # Prepare data
        # --------------------------------------------------
        allocation = self.allocation.copy()

        allocation["year_dt"] = pd.to_datetime(allocation["year"],
            format="mixed",errors="coerce", )

        allocation = allocation.sort_values(
            ["company_id", "year_dt"] )
       

        # --------------------------------------------------
        # Latest record for every company
        # --------------------------------------------------
        latest = ( allocation.groupby("company_id", as_index=False)
            .tail(1) )

        # --------------------------------------------------
        # Distribution
        # --------------------------------------------------
        distribution = (latest["capital_allocation_label"]
            .value_counts(dropna=False).reset_index())          

        distribution.columns = [ "capital_allocation_label", "company_count",]

        distribution["percentage"] = (
            distribution["company_count"] / distribution["company_count"].sum()* 100
        ).round(2)   

        # --------------------------------------------------
        # Reporting period
        # --------------------------------------------------
        latest_period = (latest["year_dt"]
            .max().strftime("%b %Y"))
      
            
            

        distribution.insert(
            0,
            "latest_reporting_period",
            latest_period,
        )

        distribution = distribution.sort_values("company_count",
            ascending=False,
        )

        distribution.to_csv( self.output_dir /  "capital_allocation_distribution.csv",
            index=False,
        )

        # --------------------------------------------------
        # Logging
        # --------------------------------------------------
        logger.info("Capital allocation distribution saved.")
 
        logger.info(f"Latest reporting period : {latest_period}" )
        
        logger.info(f"Companies mapped : {len(latest)}" )
            
        logger.info(f"Patterns : {len(distribution)}" )

        return distribution

        
    def _merge_cashflow_intelligence(self):
        """
        Merge the latest capital allocation label for each company into
        cashflow_intelligence.xlsx.

        Output
        ------
        Updated cashflow_intelligence.xlsx
        """
        logger.info("Updating Cash Flow Intelligence..." )

        # --------------------------------------------------
        # Prepare allocation data
        # --------------------------------------------------
        allocation = self.allocation.copy()

        allocation["year_dt"] = pd.to_datetime( allocation["year"],
            format="mixed",
            errors="coerce",
        )   

        allocation["company_id"] = ( allocation["company_id"].astype(str)
            .str.strip().str.upper() )
      
        allocation = allocation.sort_values(
            ["company_id", "year_dt"]
        )

        # --------------------------------------------------
        # Latest record for each company
        # --------------------------------------------------

        latest = ( allocation.groupby("company_id", as_index=False)
            .tail(1)[
                [
                    "company_id",
                    "capital_allocation_label",
                ]
            ]  )
        
        # --------------------------------------------------
        # Preparing cashflow data
        # --------------------------------------------------
        cashflow = self.cashflow.copy()

        cashflow["company_id"] = ( cashflow["company_id"].astype(str)
            .str.strip() .str.upper()
        )
   
        # Removing existing column if present
        if "capital_allocation_label" in cashflow.columns:

            cashflow.drop(columns=["capital_allocation_label"],
                inplace=True,
            )
                
        # --------------------------------------------------
        # Merge
        # --------------------------------------------------
        cashflow = cashflow.merge( latest, how="left",
            on="company_id",
        )

        # --------------------------------------------------
        # Missing labels
        # --------------------------------------------------
        missing = cashflow["capital_allocation_label"].isna().sum()

        if missing > 0:

            logger.warning(f"{missing} companies have no capital allocation label." )

            cashflow[
                cashflow["capital_allocation_label"].isna()
            ].to_csv(self.output_dir /"missing_capital_allocation.csv",
                index=False,)

        else:

            logger.info( "All companies mapped successfully." )

        #-------------------------------------------------
        # Save
        # --------------------------------------------------
        cashflow.to_excel(self.output_dir /
            "cashflow_intelligence.xlsx",index=False  ),
    
        self.cashflow = cashflow

        logger.info(f"Companies merged : {len(latest)}")

        logger.info("Cash Flow Intelligence updated successfully.")
        
        return cashflow

    def _generate_pattern_changes(self):
        """
        Generate a report of companies whose capital allocation
        pattern changed year-over-year.

        Output
        ------
        pattern_changes.csv
        """

        logger.info("Generating pattern change report...")

        allocation = self.allocation.copy()

        allocation = allocation.sort_values(
            ["company_id", "year"]
        )
        changes = []

        for company_id, df in allocation.groupby("company_id"):

            df = df.sort_values("year").reset_index(drop=True)

            company_name = None

            if "company_name" in df.columns:
                company_name = df.loc[0, "company_name"]

            previous_pattern = None

            for _, row in df.iterrows():

                current_pattern = row["capital_allocation_label"]

                if previous_pattern is not None:

                    if previous_pattern != current_pattern:

                        changes.append(
                            {
                                "company_id": company_id,
                                "company_name": company_name,
                                "year": row["year"],
                                "previous_pattern": previous_pattern,
                                "current_pattern": current_pattern,
                            }
                        )

                previous_pattern = current_pattern

        pattern_changes = pd.DataFrame(changes)

        pattern_changes.to_csv(
            self.output_dir / "pattern_changes.csv",index=False,)

        logger.info(f"Pattern changes detected: {len(pattern_changes)}")

        return pattern_changes


    def run(self):
        """
        Execute the complete Capital Allocation Summary Engine.
        """

        logger.info("=" * 60)
        logger.info("Capital Allocation Summary Started")
        logger.info("=" * 60)

        verification = self._verify_completeness()

        distribution = self._generate_distribution()

        cashflow = self._merge_cashflow_intelligence()

        pattern_changes = self._generate_pattern_changes()

        logger.info("=" * 60)
        logger.info("Capital Allocation Summary Completed")
        logger.info("=" * 60)

        return {
            "verification": verification,
            "distribution": distribution,
            "cashflow": cashflow,
            "pattern_changes": pattern_changes,
        }