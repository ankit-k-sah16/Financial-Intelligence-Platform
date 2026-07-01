from src.etl.loader import ExcelLoader
from src.etl.normalizer import DataNormalizer
from src.etl.db_loader import DatabaseLoader
def run_pipeline():
    loader=ExcelLoader("data/raw")
    db=DatabaseLoader()

    FILE_MAPPING = {
        "stg_analysis": "analysis.xlsx",
        "stg_balancesheet": "balancesheet.xlsx",
        "stg_cashflow": "cashflow.xlsx",
        "stg_companies": "companies.xlsx",
        "stg_documents": "documents.xlsx",
        "stg_profit_loss": "profitandloss.xlsx",
        "stg_pros_cons": "prosandcons.xlsx"
    }

    for table_name, file_name in FILE_MAPPING.items():
        print(f"Processing {file_name}.....")

        #Loading 
        df=loader.load_file(file_name)

        #Normalizing
        df=DataNormalizer.clean_column_names(df)

        if "year" in df.columns:
            df['year']=df['year'].apply(DataNormalizer.normalize_year)

        if "ticker" in df.columns:
            df['ticker']=df['ticker'].apply(DataNormalizer.normalize_ticker)

        db.load_table(df, table_name)


