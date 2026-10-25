
import pytest
from datetime import datetime

from app.calculation import Calculation, CalculationFactory
from app.exceptions import OperationError, ValidationError


@pytest.mark.parametrize("operation,a,b,expected", [
    ("add", 5, 3, 8),
    ("subtract", 10, 3, 7),
    ("multiply", 4, 3, 12),
    ("divide", 10, 2, 5),
    ("power", 2, 3, 8),
    ("root", 27, 3, 3),
    ("modulus", 10, 3, 1),
    ("int_divide", 10, 3, 3),
    ("percent", 25, 100, 25),
    ("abs_diff", 5, 10, 5),
])
def test_factory_operations(operation, a, b, expected):
    calculation = CalculationFactory.create(operation, a, b)

    assert isinstance(calculation, Calculation)
    assert calculation.operation == operation
    assert calculation.a == a
    assert calculation.b == b
    assert calculation.result == pytest.approx(expected)


def test_factory_invalid_operation():
    with pytest.raises(OperationError):
        CalculationFactory.create("unknown", 5, 3)


def test_factory_division_by_zero():
    with pytest.raises(OperationError):
        CalculationFactory.create("divide", 5, 0)


def test_factory_invalid_input():
    with pytest.raises(ValidationError):
        CalculationFactory.create("add", "hello", 3)


def test_factory_timestamp():
    calculation = CalculationFactory.create("add", 2, 3)

    assert calculation.timestamp
    assert datetime.fromisoformat(calculation.timestamp)
