
import pytest

from app.calculation import CalculationFactory
from app.calculator_memento import CalculatorMemento
from app.history import CalculationHistory
from app.exceptions import OperationError, ValidationError


def make_calculation(a, b):
    return CalculationFactory.create("add", a, b)


def test_empty_history():
    history = CalculationHistory()
    assert history.get_history() == []


def test_add_calculation():
    history = CalculationHistory()
    calculation = make_calculation(5, 3)

    history.add(calculation)

    assert history.get_history() == [calculation]


def test_multiple_calculations():
    history = CalculationHistory()

    history.add(make_calculation(5, 3))
    history.add(make_calculation(10, 2))

    assert len(history.get_history()) == 2


def test_undo():
    history = CalculationHistory()

    history.add(make_calculation(5, 3))
    history.add(make_calculation(10, 2))

    history.undo()

    assert len(history.get_history()) == 1


def test_redo():
    history = CalculationHistory()

    history.add(make_calculation(5, 3))
    history.add(make_calculation(10, 2))

    history.undo()
    history.redo()

    assert len(history.get_history()) == 2


def test_multiple_undo():
    history = CalculationHistory()

    history.add(make_calculation(5, 3))
    history.add(make_calculation(10, 2))

    history.undo()
    history.undo()

    assert history.get_history() == []


def test_undo_empty():
    history = CalculationHistory()

    with pytest.raises(OperationError):
        history.undo()


def test_redo_empty():
    history = CalculationHistory()

    with pytest.raises(OperationError):
        history.redo()


def test_new_calculation_clears_redo():
    history = CalculationHistory()

    history.add(make_calculation(5, 3))
    history.undo()
    history.add(make_calculation(10, 2))

    with pytest.raises(OperationError):
        history.redo()


def test_clear():
    history = CalculationHistory()

    history.add(make_calculation(5, 3))
    history.clear()

    assert history.get_history() == []


def test_undo_clear():
    history = CalculationHistory()

    history.add(make_calculation(5, 3))
    history.clear()
    history.undo()

    assert len(history.get_history()) == 1


def test_max_history_size():
    history = CalculationHistory(max_size=2)

    history.add(make_calculation(1, 1))
    history.add(make_calculation(2, 2))
    history.add(make_calculation(3, 3))

    assert len(history.get_history()) == 2
    assert history.get_history()[0].result == 4


@pytest.mark.parametrize("size", [0, -1, 2.5, True])
def test_invalid_max_size(size):
    with pytest.raises(ValidationError):
        CalculationHistory(max_size=size)


def test_invalid_calculation():
    history = CalculationHistory()

    with pytest.raises(ValidationError):
        history.add("invalid")


def test_history_returns_copy():
    history = CalculationHistory()
    history.add(make_calculation(5, 3))

    copied_history = history.get_history()
    copied_history.clear()

    assert len(history.get_history()) == 1


def test_replace_history():
    history = CalculationHistory()
    calculation = make_calculation(5, 3)

    history.replace([calculation])

    assert history.get_history() == [calculation]


def test_undo_replace():
    history = CalculationHistory()

    history.add(make_calculation(1, 1))
    history.replace([make_calculation(5, 3)])
    history.undo()

    assert history.get_history()[0].result == 2


def test_invalid_replace():
    history = CalculationHistory()

    with pytest.raises(ValidationError):
        history.replace(["invalid"])


def test_memento_snapshot():
    calculation = make_calculation(5, 3)
    memento = CalculatorMemento((calculation,))

    assert memento.calculations == (calculation,)
