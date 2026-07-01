from pathlib import Path
import sys

from src.validation.ratio_validator import RatioValidator

def test_opm_cross_check_mismatch():
    validator=RatioValidator()

    result=validator.validate_operating_profit_margin(
        operating_profit=300,
        sales=1000,
        stored_opm=35,
        tolerance=1
    )
    assert result["status"] == "FAIL"