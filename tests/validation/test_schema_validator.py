from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.validation.schema_validator import SchemaValidator


def test_validator_creation():

    validator = SchemaValidator()

    assert validator is not None


def test_failure_log_initialization():

    validator = SchemaValidator()

    assert isinstance(
        validator.failures,
        list
    )