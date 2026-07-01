import pandas as pd
from datetime import datetime
from src.validation.schema_registry import SCHEMAS


class SchemaValidator:

    def __init__(self):
        self.failures = []

    def log_failure(
        self,
        dataset,
        rule,
        column,
        failed_rows,
        severity="HIGH"
    ):
        self.failures.append({
            "dataset": dataset,
            "rule": rule,
            "column": column,
            "failed_rows": failed_rows,
            "severity": severity
        })

    def validate(
        self,
        dataset_name,
        df,
        companies_df=None
    ):

        schema = SCHEMAS.get(dataset_name)

        if not schema:
            return

        self._check_empty_dataset(
            dataset_name,
            df
        )

        self._check_required_columns(
            dataset_name,
            df,
            schema
        )

        self._check_duplicate_columns(
            dataset_name,
            df
        )

        self._check_primary_key(
            dataset_name,
            df,
            schema
        )

        self._check_year_column(
            dataset_name,
            df
        )

        if (
            companies_df is not None
            and dataset_name != "companies"
        ):
            self._check_foreign_key(
                dataset_name,
                df,
                companies_df
            )

    def _check_empty_dataset(
        self,
        dataset_name,
        df
    ):

        if df.empty:

            self.log_failure(
                dataset_name,
                "empty_dataset",
                "",
                0,
                "CRITICAL"
            )

    def _check_required_columns(
        self,
        dataset_name,
        df,
        schema
    ):

        required_cols = schema.get(
            "required_columns",
            []
        )

        missing_cols = [
            col
            for col in required_cols
            if col not in df.columns
        ]

        if missing_cols:

            self.log_failure(
                dataset_name,
                "missing_columns",
                ",".join(missing_cols),
                len(missing_cols),
                "CRITICAL"
            )

    def _check_duplicate_columns(
        self,
        dataset_name,
        df
    ):

        duplicate_cols = (
            df.columns[
                df.columns.duplicated()
            ]
            .tolist()
        )

        if duplicate_cols:

            self.log_failure(
                dataset_name,
                "duplicate_columns",
                ",".join(duplicate_cols),
                len(duplicate_cols),
                "HIGH"
            )

    def _check_primary_key(
        self,
        dataset_name,
        df,
        schema
    ):

        primary_keys = schema.get(
            "primary_key",
            []
        )

        if not primary_keys:
            return

        # Null PK check
        null_rows = (
            df[primary_keys]
            .isnull()
            .any(axis=1)
            .sum()
        )

        if null_rows > 0:

            self.log_failure(
                dataset_name,
                "null_primary_key",
                ",".join(primary_keys),
                int(null_rows),
                "CRITICAL"
            )

        # Duplicate PK check
        duplicate_rows = (
            df.duplicated(
                subset=primary_keys
            )
            .sum()
        )

        if duplicate_rows > 0:

            self.log_failure(
                dataset_name,
                "duplicate_primary_key",
                ",".join(primary_keys),
                int(duplicate_rows),
                "CRITICAL"
            )

    def _check_foreign_key(
    self,
    dataset_name,
    df,
    companies_df
):

        if "company_id" not in df.columns:
            return

        valid_ids = set(
            companies_df["id"]
            .astype(str)
            .str.strip()
        )

        invalid_mask = (
            ~df["company_id"]
            .astype(str)
            .str.strip()
            .isin(valid_ids)
        )

        invalid_rows = invalid_mask.sum()

        

        if invalid_rows > 0:

            self.log_failure(
                dataset_name,
                "invalid_company_id",
                "company_id",
                int(invalid_rows),
                "CRITICAL"
            )
    def _check_year_column(
    self,
    dataset_name,
    df
):

        if "year" not in df.columns:
            return

        current_year = datetime.now().year

        year_series = pd.to_numeric(
            df["year"],
            errors="coerce"
        )

        # Missing years
        null_years = year_series.isnull().sum()

        # Invalid years
        invalid_years = (
            (year_series < 2000)
            |
            (year_series > current_year)
        ).sum()

        if null_years > 0:

            self.log_failure(
                dataset_name,
                "missing_year",
                "year",
                int(null_years),
                "HIGH"
            )

        if invalid_years > 0:

            self.log_failure(
                dataset_name,
                "invalid_year",
                "year",
                int(invalid_years),
                "HIGH"
            )

    def save_failures(
        self,
        output_path
    ):

        if not self.failures:

            print(
                "✓ No validation failures found"
            )
            return

        pd.DataFrame(
            self.failures
        ).to_csv(
            output_path,
            index=False
        )

        print(
            f"Validation report saved to "
            f"{output_path}"
        )

