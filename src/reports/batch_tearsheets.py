"""
Batch Company Tear Sheet Generator
N100 Financial Intelligence Platform
"""

from pathlib import Path
import logging
import pandas as pd
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.reports.tearsheet import CompanyTearSheet

logger = logging.getLogger(__name__)


class BatchTearSheetGenerator:
    """
    Generate tear sheets for all companies.
    """

    def __init__(
        self,
        companies_df,
        profitloss_df,
        balancesheet_df,
        cashflow_df,
        proscons_df,
        intelligence_df,
        output_dir,
    ):

        self.companies_df = companies_df.copy()

        # --------------------------------------------------
        # Normalize company identifier
        # --------------------------------------------------
        self.companies_df.columns = (
            self.companies_df.columns
            .str.strip()
            .str.lower()
        )

        if "company_id" not in self.companies_df.columns:

            if "id" in self.companies_df.columns:

                self.companies_df.rename(
                    columns={"id": "company_id"},
                    inplace=True,
                )

        self.pnl_df = profitloss_df.copy()

        self.balance_df = balancesheet_df.copy()

        self.cashflow_df = cashflow_df.copy()

        self.proscons_df = proscons_df.copy()

        self.intelligence_df = intelligence_df.copy()

        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.generator = CompanyTearSheet(
            companies_df=self.companies_df,
            profitloss_df=self.pnl_df,
            balancesheet_df=self.balance_df,
            cashflow_df=self.cashflow_df,
            proscons_df=self.proscons_df,
            cashflow_intelligence_df=self.intelligence_df,
            output_dir=self.output_dir,
        )

    # ---------------------------------------------------------
    # Generate Single Company
    # ---------------------------------------------------------

    def generate_company(
        self,
        company_id,
    ):
        """
        Generate one company tear sheet.
        """

        output_file = (
            self.output_dir /
            f"{company_id}_tearsheet.pdf"
        )

        try:

            self.generator.build_company_tearsheet(
                company_id=company_id,
                output_path=str(output_file),
            )

            logger.info(
                f"Generated : {company_id}"
            )

            return {
                "company_id": company_id,
                "status": "SUCCESS",
                "file": str(output_file),
            }

        except Exception as e:

            logger.exception(
                f"{company_id} failed"
            )

            return {
                "company_id": company_id,
                "status": "FAILED",
                "file": None,
                "error": str(e),
            }    

    # ---------------------------------------------------------
    # Company List
    # ---------------------------------------------------------

    def company_ids(self):
        """
        Return unique company identifiers.
        """

        if "company_id" not in self.companies_df.columns:
            raise KeyError(
                "companies dataframe has no company_id column."
            )

        return (
            self.companies_df["company_id"]
            .dropna()
            .astype(str)
            .str.strip()
            .sort_values()
            .unique()
            .tolist()
        )
    # ---------------------------------------------------------
    # Generate All Tear Sheets
    # ---------------------------------------------------------

    def generate_all(self):
        """
        Generate tear sheets for every company.
        """

        companies = self.company_ids()

        logger.info(
            f"Generating {len(companies)} tear sheets..."
        )

        results = []

        for index, company_id in enumerate(
            companies,
            start=1,
        ):

            logger.info(
                f"[{index}/{len(companies)}] {company_id}"
            )

            result = self.generate_company(
                company_id,
            )

            results.append(result)

        report = pd.DataFrame(results)

        report_path = (
            self.output_dir /
            "generation_report.csv"
        )

        report.to_csv(
            report_path,
            index=False,
        )

        logger.info(
            f"Report saved : {report_path}"
        )

        return report     

    # ---------------------------------------------------------
    # Generate Selected Companies
    # ---------------------------------------------------------

    def generate_selected(
        self,
        company_ids,
    ):
        """
        Generate tear sheets only for
        selected companies.
        """

        results = []

        for company in company_ids:

            results.append(
                self.generate_company(
                    company,
                )
            )

        return pd.DataFrame(results)
    