
import pandas as pd
import pytest

from app.calculator_config import CalculatorConfig
from app.calculation import CalculationFactory
from app.exceptions import HistoryError
from app.history_storage import HistoryStorage


def make_storage(tmp_path):
    config = CalculatorConfig()
    config.history_file = tmp_path / "history" / "calculations.csv"
    return HistoryStorage(config)


def make_calculation(a, b):
    return CalculationFactory.create("add", a, b)


def write_test_csv(storage, content):
    storage.path.parent.mkdir(
        parents=True, exist_ok=True
    )
    storage.path.write_text(
        content, encoding="utf-8"
    )


def test_save_creates_csv(tmp_path):
    storage = make_storage(tmp_path)
    storage.save([make_calculation(5, 3)])

    assert storage.path.exists()


def test_csv_columns(tmp_path):
    storage = make_storage(tmp_path)
    storage.save([make_calculation(5, 3)])

    dataframe = pd.read_csv(storage.path)

    assert list(dataframe.columns) == [
        "operation", "operands", "result", "timestamp"
    ]


def test_save_and_load(tmp_path):
    storage = make_storage(tmp_path)

    calculations = [
        make_calculation(5, 3),
        make_calculation(10, 2),
    ]

    storage.save(calculations)
    loaded = storage.load()

    assert len(loaded) == 2
    assert loaded[0].result == 8
    assert loaded[1].result == 12
    assert loaded[0].operation == "add"


def test_empty_history(tmp_path):
    storage = make_storage(tmp_path)

    storage.save([])
    loaded = storage.load()

    assert loaded == []


def test_missing_file(tmp_path):
    storage = make_storage(tmp_path)

    with pytest.raises(HistoryError):
        storage.load()


def test_missing_columns(tmp_path):
    storage = make_storage(tmp_path)

    write_test_csv(
        storage,
        "wrong_column,result\nadd,8\n"
    )

    with pytest.raises(HistoryError):
        storage.load()


def test_invalid_json(tmp_path):
    storage = make_storage(tmp_path)

    write_test_csv(
        storage,
        "operation,operands,result,timestamp\n"
        "add,invalid,8,2026-10-25T12:00:00\n"
    )

    with pytest.raises(HistoryError):
        storage.load()


def test_invalid_result(tmp_path):
    storage = make_storage(tmp_path)

    write_test_csv(
        storage,
        "operation,operands,result,timestamp\n"
        'add,"[5, 3]",wrong,2026-10-25T12:00:00\n'
    )

    with pytest.raises(HistoryError):
        storage.load()


def test_unknown_operation(tmp_path):
    storage = make_storage(tmp_path)

    write_test_csv(
        storage,
        "operation,operands,result,timestamp\n"
        'unknown,"[5, 3]",8,2026-10-25T12:00:00\n'
    )

    with pytest.raises(HistoryError):
        storage.load()


def test_invalid_timestamp(tmp_path):
    storage = make_storage(tmp_path)

    write_test_csv(
        storage,
        "operation,operands,result,timestamp\n"
        'add,"[5, 3]",8,not-a-date\n'
    )

    with pytest.raises(HistoryError):
        storage.load()


def test_invalid_calculation_on_save(tmp_path):
    storage = make_storage(tmp_path)

    with pytest.raises(HistoryError):
        storage.save(["invalid"])


def test_invalid_operands(tmp_path):
    storage = make_storage(tmp_path)

    write_test_csv(
        storage,
        "operation,operands,result,timestamp\n"
        'add,"[true, 3]",8,2026-10-25T12:00:00\n'
    )

    with pytest.raises(HistoryError):
        storage.load()
