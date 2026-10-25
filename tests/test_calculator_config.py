
import pytest

from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError


def test_config_default_values():
    config = CalculatorConfig()

    assert config.max_history_size > 0
    assert config.precision >= 0
    assert config.max_input_value > 0
    assert config.default_encoding


def test_config_paths():
    config = CalculatorConfig()

    assert config.log_dir.is_absolute()
    assert config.history_dir.is_absolute()
    assert config.log_file.is_absolute()
    assert config.history_file.is_absolute()


def test_config_override(monkeypatch):
    monkeypatch.setenv(
        "CALCULATOR_MAX_HISTORY_SIZE", "20"
    )

    config = CalculatorConfig()

    assert config.max_history_size == 20


def test_auto_save_false(monkeypatch):
    monkeypatch.setenv(
        "CALCULATOR_AUTO_SAVE", "false"
    )

    config = CalculatorConfig()

    assert config.auto_save is False


@pytest.mark.parametrize("value", ["0", "-1", "abc"])
def test_invalid_history_size(monkeypatch, value):
    monkeypatch.setenv(
        "CALCULATOR_MAX_HISTORY_SIZE", value
    )

    with pytest.raises(ValidationError):
        CalculatorConfig()


def test_invalid_precision(monkeypatch):
    monkeypatch.setenv(
        "CALCULATOR_PRECISION", "-1"
    )

    with pytest.raises(ValidationError):
        CalculatorConfig()


def test_invalid_max_input(monkeypatch):
    monkeypatch.setenv(
        "CALCULATOR_MAX_INPUT_VALUE", "-100"
    )

    with pytest.raises(ValidationError):
        CalculatorConfig()


def test_invalid_auto_save(monkeypatch):
    monkeypatch.setenv(
        "CALCULATOR_AUTO_SAVE", "maybe"
    )

    with pytest.raises(ValidationError):
        CalculatorConfig()


def test_invalid_encoding(monkeypatch):
    monkeypatch.setenv(
        "CALCULATOR_DEFAULT_ENCODING", "unknown_encoding"
    )

    with pytest.raises(ValidationError):
        CalculatorConfig()
