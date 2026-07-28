from pathlib import Path
from dotenv import load_dotenv
import os

ROOT_DIR = Path(__file__).resolve().parent.parent

load_dotenv(ROOT_DIR / "config" / ".env")

DB_PATH = ROOT_DIR / os.getenv("DB_PATH")

RAW_DATA_DIR = ROOT_DIR / os.getenv("RAW_DATA_PATH")

SUPPORTING_DATA_DIR = ROOT_DIR / os.getenv("SUPPORTING_DATA_PATH")

OUTPUT_DIR = ROOT_DIR / os.getenv("OUTPUT_PATH")

REPORT_OUTPUT_DIR =  ROOT_DIR/ os.getenv("REPORT_OUTPUT_PATH")


    
    

  