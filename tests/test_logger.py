
import pytest

from app.calculator_config import CalculatorConfig
from app.calculation import CalculationFactory
from app.logger import Logger, LoggingObserver


def make_logger(tmp_path):
    """Create a logger using a temporary test folder."""
    config = CalculatorConfig()
    config.log_file = tmp_path / "logs" / "calculator.log"

    logger = Logger(config)

    return logger, config


def test_logger_creates_file(tmp_path):
    logger, config = make_logger(tmp_path)

    assert config.log_file.exists()


def test_logger_info(tmp_path):
    logger, config = make_logger(tmp_path)

    logger.info("Calculator started")

    content = config.log_file.read_text()

    assert "Calculator started" in content
    assert "INFO" in content


def test_logger_warning(tmp_path):
    logger, config = make_logger(tmp_path)

    logger.warning("Invalid input")

    content = config.log_file.read_text()

    assert "Invalid input" in content
    assert "WARNING" in content


def test_logger_error(tmp_path):
    logger, config = make_logger(tmp_path)

    logger.error("Calculation failed")

    content = config.log_file.read_text()

    assert "Calculation failed" in content
    assert "ERROR" in content


def test_logging_observer(tmp_path):
    logger, config = make_logger(tmp_path)

    observer = LoggingObserver(logger)
    calculation = CalculationFactory.create(
        "add", 5, 3
    )

    observer.update(calculation)

    content = config.log_file.read_text()

    assert "Operation: add" in content
    assert "Operands: 5, 3" in content
    assert "Result: 8" in content


def test_no_duplicate_handlers(tmp_path):
    logger, config = make_logger(tmp_path)

    # Create another logger for the same file.
    second_logger = Logger(config)

    logger.info("Test message")

    content = config.log_file.read_text()

    assert content.count("Test message") == 1


@pytest.mark.parametrize("operation,a,b", [
    ("add", 5, 3),
    ("subtract", 5, 3),
    ("multiply", 5, 3),
    ("divide", 6, 3),
    ("power", 2, 3),
    ("root", 27, 3),
    ("modulus", 10, 3),
    ("int_divide", 10, 3),
    ("percent", 25, 100),
    ("abs_diff", 5, 10),
])
def test_logging_all_operations(
    tmp_path, operation, a, b
):
    logger, config = make_logger(tmp_path)

    calculation = CalculationFactory.create(
        operation, a, b
    )

    logger.log_calculation(calculation)

    content = config.log_file.read_text()

    assert f"Operation: {operation}" in content
    assert "Result:" in content
