from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.etl.normalizer import DataNormalizer


def test_normalize_year():

    assert (
        DataNormalizer.normalize_year(
            "Mar-24"
        ) == 2024
    )


def test_normalize_ticker():

    assert (
        DataNormalizer.normalize_ticker(
            " tcs "
        ) == "TCS"
    )