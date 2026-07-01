from pathlib import Path
from src.etl.loader import ExcelLoader
from src.etl.normalizer import DataNormalizer
from src.etl.db_loader import DatabaseLoader
from src.validation.schema_validator import SchemaValidator


def run_pipeline():

    core_loader = ExcelLoader("data/raw")

    support_loader = ExcelLoader(
        "data/supporting"
    )
    db = DatabaseLoader()
    validator = SchemaValidator()

    CORE_FILES = {
    "companies": "companies.xlsx",
    "analysis": "analysis.xlsx",
    "balancesheet": "balancesheet.xlsx",
    "cashflow": "cashflow.xlsx",
    "documents": "documents.xlsx",
    "profitandloss": "profitandloss.xlsx",
    "prosandcons": "prosandcons.xlsx"
}   
    core_datasets = {}

    for name, file in CORE_FILES.items():

        core_datasets[name] = core_loader.load_file(
            file,
            header=1
        )


    SUPPORT_FILES = {
        "financial_ratios": "financial_ratios.xlsx",
        "market_cap": "market_cap.xlsx",
        "peer_groups": "peer_groups.xlsx",
        "sectors": "sectors.xlsx",
        "stock_prices": "stock_prices.xlsx"
    }
    support_datasets = {}
    
    for name, file in SUPPORT_FILES.items():

        support_datasets[name] = support_loader.load_file(
            file,
            header=0
        )


    LOAD_ORDER = [

        "companies",
        "sectors",
        "peer_groups",

        "analysis",
        "balancesheet",
        "cashflow",
        "profitandloss",

        "financial_ratios",
        "market_cap",
        "stock_prices",

        "documents",
        "prosandcons"
    ]


    # Load all files once
    datasets = {
    **core_datasets,
    **support_datasets
}

    companies_df = DataNormalizer.clean_column_names(
    datasets["companies"].copy()
)
    audit_rows = []
     
    for dataset_name in LOAD_ORDER:

        df = datasets[dataset_name]

        # Normalize
        df = DataNormalizer.clean_column_names(df)

        

        if "year" in df.columns:
            df["year"] = df["year"].apply(
                DataNormalizer.normalize_year
            )

    
        # Validate
        validator.validate(
            dataset_name=dataset_name,
            df=df,
            companies_df=companies_df
        )

        # Load to DB
        db.load_table(
            df,
            f"stg_{dataset_name}"
        )
        audit_rows.append(
    {
        "table_name": f"stg_{dataset_name}",
        "rows_loaded": len(df),
        "status": "SUCCESS"
    }
)
    
    # Save validation report
    Path("output").mkdir(
        exist_ok=True
    )

    validator.save_failures(
        "output/validation_failures.csv"
          )
    
    import pandas as pd

    pd.DataFrame(
        audit_rows
    ).to_csv(
        "output/load_audit.csv",
        index=False
)
    
    print("Load audit saved to output/load_audit.csv")
    

    print("Pipeline completed successfully.")



if __name__ == "__main__":
    run_pipeline()  

