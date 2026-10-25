
import pytest

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError


def make_calculator(tmp_path, auto_save=True):
    """Create a calculator using temporary files."""
    config = CalculatorConfig()

    config.log_file = tmp_path / "logs" / "calculator.log"
    config.history_file = (
        tmp_path / "history" / "calculations.csv"
    )
    config.auto_save = auto_save

    return Calculator(config)


def test_calculator_add(tmp_path):
    calculator = make_calculator(tmp_path)

    result = calculator.calculate("add", 5, 3)

    assert result.result == 8
    assert len(calculator.get_history()) == 1


def test_calculator_multiple_operations(tmp_path):
    calculator = make_calculator(tmp_path)

    calculator.calculate("add", 5, 3)
    calculator.calculate("multiply", 4, 2)
    calculator.calculate("power", 2, 3)

    assert len(calculator.get_history()) == 3


def test_automatic_logging(tmp_path):
    calculator = make_calculator(tmp_path)

    calculator.calculate("add", 5, 3)

    content = calculator.config.log_file.read_text()

    assert "Operation: add" in content
    assert "Result: 8" in content


def test_automatic_save(tmp_path):
    calculator = make_calculator(tmp_path)

    calculator.calculate("add", 5, 3)

    assert calculator.config.history_file.exists()

    loaded = calculator.storage.load()

    assert len(loaded) == 1
    assert loaded[0].result == 8


def test_auto_save_disabled(tmp_path):
    calculator = make_calculator(
        tmp_path, auto_save=False
    )

    calculator.calculate("add", 5, 3)

    assert not calculator.config.history_file.exists()


def test_manual_save_and_load(tmp_path):
    first = make_calculator(
        tmp_path, auto_save=False
    )

    first.calculate("add", 5, 3)
    first.save()

    second = make_calculator(
        tmp_path, auto_save=False
    )

    second.load()

    assert len(second.get_history()) == 1
    assert second.get_history()[0].result == 8


def test_calculator_undo_redo(tmp_path):
    calculator = make_calculator(tmp_path)

    calculator.calculate("add", 5, 3)
    calculator.calculate("multiply", 4, 2)

    calculator.undo()

    assert len(calculator.get_history()) == 1
    assert len(calculator.storage.load()) == 1

    calculator.redo()

    assert len(calculator.get_history()) == 2
    assert len(calculator.storage.load()) == 2


def test_calculator_clear(tmp_path):
    calculator = make_calculator(tmp_path)

    calculator.calculate("add", 5, 3)
    calculator.clear()

    assert calculator.get_history() == []
    assert calculator.storage.load() == []


def test_calculator_precision(tmp_path):
    calculator = make_calculator(tmp_path)

    result = calculator.calculate("divide", 1, 3)

    assert result.result == 0.333333


@pytest.mark.parametrize("value", [
    1000001,
    -1000001,
])
def test_calculator_input_range(tmp_path, value):
    calculator = make_calculator(tmp_path)

    with pytest.raises(ValidationError):
        calculator.calculate("add", value, 3)


@pytest.mark.parametrize("value", [
    "hello",
    True,
    float("nan"),
])
def test_calculator_invalid_input(tmp_path, value):
    calculator = make_calculator(tmp_path)

    with pytest.raises(ValidationError):
        calculator.calculate("add", value, 3)


def test_calculator_invalid_operation(tmp_path):
    calculator = make_calculator(tmp_path)

    with pytest.raises(OperationError):
        calculator.calculate("unknown", 5, 3)


def test_register_and_remove_observer(tmp_path):
    calculator = make_calculator(tmp_path)

    class TestObserver:
        def __init__(self):
            self.events = []

        def update(self, calculation, history):
            self.events.append(calculation)

    observer = TestObserver()

    calculator.register_observer(observer)
    calculator.calculate("add", 5, 3)

    assert len(observer.events) == 1

    calculator.remove_observer(observer)
    calculator.calculate("add", 2, 3)

    assert len(observer.events) == 1


def test_invalid_observer(tmp_path):
    calculator = make_calculator(tmp_path)

    with pytest.raises(ValidationError):
        calculator.register_observer("invalid")
