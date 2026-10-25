
import pytest
from app.operations import Operations


@pytest.mark.parametrize("a, b, expected", [
    (5, 3, 8),
    (-5, 3, -2),
    (0, 0, 0),
])
def test_add(a, b, expected):
    assert Operations.add(a, b) == expected


def test_subtract():
    assert Operations.subtract(10, 4) == 6


def test_multiply():
    assert Operations.multiply(5, 3) == 15


def test_divide():
    assert Operations.divide(10, 2) == 5


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        Operations.divide(10, 0)


@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 8),
    (2, -2, 0.25),
    (5, 0, 1),
])
def test_power(a, b, expected):
    assert Operations.power(a, b) == expected


def test_power_invalid():
    with pytest.raises(ValueError):
        Operations.power(-2, 0.5)


@pytest.mark.parametrize("a, b, expected", [
    (27, 3, 3),
    (16, 2, 4),
    (-8, 3, -2),
])
def test_root(a, b, expected):
    assert Operations.root(a, b) == pytest.approx(expected)


def test_root_invalid():
    with pytest.raises(ValueError):
        Operations.root(-8, 2)


def test_root_zero_degree():
    with pytest.raises(ValueError):
        Operations.root(8, 0)


def test_modulus():
    assert Operations.modulus(10, 3) == 1


def test_int_divide():
    assert Operations.int_divide(10, 3) == 3
    assert Operations.int_divide(-10, 3) == -3


def test_percent():
    assert Operations.percent(25, 100) == 25


def test_abs_diff():
    assert Operations.abs_diff(5, 10) == 5


@pytest.mark.parametrize("operation", [
    Operations.modulus,
    Operations.int_divide,
    Operations.percent,
])
def test_zero_division(operation):
    with pytest.raises(ZeroDivisionError):
        operation(10, 0)
