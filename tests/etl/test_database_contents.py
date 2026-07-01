from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from sqlalchemy import create_engine, text
from config.setting import DB_PATH


def test_companies_loaded():

    engine = create_engine(
        f"sqlite:///{DB_PATH}"
    )

    with engine.connect() as conn:

        count = conn.execute(
            text(
                """
                SELECT COUNT(*)
                FROM stg_companies
                """
            )
        ).scalar()

    assert count > 0