from pathlib import Path
import sys


from src.analytics.cagr import CAGR_calculator


def test_normal_cagr():

    value, flag = CAGR_calculator.calculate_cagr(
        100,
        200,
        5
    )

    assert round(value, 2) == 14.87
    assert flag == "OK"


def test_decline_to_loss():

    value, flag = CAGR_calculator.calculate_cagr(
        100,
        -50,
        5
    )

    assert value is None
    assert flag == "DECLINE_TO_LOSS"


def test_turnaround():

    value, flag = CAGR_calculator.calculate_cagr(
        -100,
        50,
        5
    )

    assert value is None
    assert flag == "TURNAROUND"


def test_both_negative():

    value, flag = CAGR_calculator.calculate_cagr(
        -100,
        -50,
        5
    )

    assert value is None
    assert flag == "BOTH_NEGATIVE"


def test_zero_base():

    value, flag = CAGR_calculator.calculate_cagr(
        0,
        100,
        5
    )

    assert value is None
    assert flag == "ZERO_BASE"


def test_insufficient_years():

    value, flag = CAGR_calculator.calculate_cagr(
        100,
        200,
        0
    )

    assert value is None
    assert flag == "INSUFFICIENT"


def test_revenue_cagr():

    value, flag = CAGR_calculator.revenue_cagr_5yr(
        500,
        1000
    )

    assert flag == "OK"


def test_pat_cagr():

    value, flag = CAGR_calculator.pat_cagr_3yr(
        100,
        200
    )

    assert flag == "OK"


def test_eps_cagr():

    value, flag = CAGR_calculator.eps_cagr_10yr(
        20,
        50
    )

    assert flag == "OK"


def test_none_values():

    value, flag = CAGR_calculator.calculate_cagr(
        None,
        100,
        5
    )

    assert value is None
    assert flag == "INSUFFICIENT"