from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.etl.db_loader import DatabaseLoader


def test_database_loader():

    db = DatabaseLoader()

    assert db.engine is not None