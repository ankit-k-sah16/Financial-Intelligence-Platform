from pathlib import Path
from dotenv import load_dotenv
import os

ROOT_DIR = Path(__file__).resolve().parent.parent

load_dotenv(ROOT_DIR / "config" / ".env")

DB_PATH = ROOT_DIR / os.getenv("DB_PATH")