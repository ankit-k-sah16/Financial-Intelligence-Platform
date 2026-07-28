"""
=========================================================
Run Analysis Text Parser
N100 Financial Intelligence Platform
=========================================================
"""

from pathlib import Path
import sys 
import logging
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.nlp.parser import AnalysisParser
# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------
logging.basicConfig(level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s")

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# File Paths
# ---------------------------------------------------------
ANALYSIS_FILE = Path("data/raw/analysis.xlsx")
    
RATIO_ENGINE_FILE = Path( "output/ratio_engine_summary.csv")
   
OUTPUT_DIR = Path( "output")  

# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
def main():

    logger.info("=" * 60)

    logger.info("Loading Analysis Dataset...")

    analysis_df = pd.read_excel( ANALYSIS_FILE,header=1 )

    analysis_df.columns = (analysis_df.columns.astype(str) .str.strip()
        .str.lower().str.replace(" ", "_"))

    # ---------------------------------------------
    if "id" in analysis_df.columns:

        analysis_df.rename(
            columns={"id": "company_id"},inplace=True)           
 
    logger.info( f"Analysis Records : {len(analysis_df)}")

    # ---------------------------------------------
    parser = AnalysisParser(output_dir=OUTPUT_DIR )

    parsed_df, failures_df = parser.parse(analysis_df)

    logger.info(f"Parsed Rows : {len(parsed_df)}")

    logger.info(f"Failed Rows : {len(failures_df)}")  

    # -------------------------------------------------
    # Ratio Engine Validation
    # -------------------------------------------------
    
    if RATIO_ENGINE_FILE.exists():

        logger.info("Loading Ratio Engine Output..." )

        ratio_df = pd.read_csv( RATIO_ENGINE_FILE)

        ratio_df.columns = (ratio_df.columns.astype(str) .str.strip() 
                            .str.lower() .str.replace(" ", "_"))
           

        validation_df = (parser.validate_against_ratio_engine( parsed_df,ratio_df ))

        logger.info( f"Validation Rows : {len(validation_df)}")

    else:

        logger.warning("Ratio Engine output not found." )

        logger.warning("Skipping CAGR validation.")

    logger.info("=" * 60)

    logger.info( "Analysis Parser Completed Successfully.")

# ---------------------------------------------------------
# Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":

    main()