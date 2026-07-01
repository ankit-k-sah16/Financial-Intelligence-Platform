from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.etl.loader import ExcelLoader


def test_loader_created():

    loader = ExcelLoader(
        "data/raw"
    )

    assert loader is not None


def test_raw_folder_exists():

    assert Path(
        "data/raw"
    ).exists()