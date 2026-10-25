
import pytest

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.repl import CalculatorREPL



def make_repl(tmp_path, auto_save=True):
    config = CalculatorConfig()
    config.log_file = tmp_path / "logs" / "calculator.log"
    config.history_file = tmp_path / "history" / "calculations.csv"
    config.auto_save = auto_save

    calculator = Calculator(config)
    output = []

    repl = CalculatorREPL(
        calculator=calculator,
        output_func=output.append
    )
    return repl, output



@pytest.mark.parametrize("command,expected", [
    ("add 5 3", "8"),
    ("subtract 5 3", "2"),
    ("multiply 5 3", "15"),
    ("divide 6 3", "2"),
    ("power 2 3", "8"),
    ("root 27 3", "3"),
    ("modulus 10 3", "1"),
    ("int_divide 10 3", "3"),
    ("percent 25 100", "25"),
    ("abs_diff 5 10", "5"),
])
def test_repl_operations(tmp_path, command, expected):
    repl, output = make_repl(tmp_path)

    repl.execute(command)

    assert output[-1] == f"Result: {expected}"


def test_repl_help(tmp_path):
    repl, output = make_repl(tmp_path)
    repl.execute("help")

    assert any("Available operations" in x for x in output)


def test_repl_history(tmp_path):
    repl, output = make_repl(tmp_path)

    repl.execute("add 5 3")
    repl.execute("history")

    assert any("add 5 3 = 8" in x for x in output)


def test_repl_undo_redo(tmp_path):
    repl, output = make_repl(tmp_path)

    repl.execute("add 5 3")
    repl.execute("undo")

    assert repl.calculator.get_history() == []

    repl.execute("redo")
    assert len(repl.calculator.get_history()) == 1


def test_repl_clear(tmp_path):
    repl, output = make_repl(tmp_path)

    repl.execute("add 5 3")
    repl.execute("clear")

    assert repl.calculator.get_history() == []



def test_repl_save_load(tmp_path):
    # Disable auto-save to test manual save/load.
    repl, output = make_repl(
        tmp_path, auto_save=False
    )

    repl.execute("add 5 3")
    repl.execute("save")
    repl.execute("clear")
    repl.execute("load")

    assert len(repl.calculator.get_history()) == 1



@pytest.mark.parametrize("command", [
    "add hello 3",
    "add 5",
    "add 5 3 2",
    "add nan 3",
])
def test_repl_invalid_input(tmp_path, command):
    repl, output = make_repl(tmp_path)

    with pytest.raises(ValidationError):
        repl.execute(command)


def test_repl_unknown_command(tmp_path):
    repl, output = make_repl(tmp_path)

    with pytest.raises(OperationError):
        repl.execute("unknown")


def test_repl_empty_command(tmp_path):
    repl, output = make_repl(tmp_path)

    assert repl.execute("") is True


def test_repl_exit(tmp_path):
    repl, output = make_repl(tmp_path)

    assert repl.execute("exit") is False
    assert output[-1] == "Goodbye!"


def test_repl_run(tmp_path):
    repl, output = make_repl(tmp_path)

    commands = iter(["add 5 3", "history", "exit"])
    repl.input_func = lambda prompt: next(commands)

    repl.run()

    assert "Goodbye!" in output
    assert any("Result: 8" in x for x in output)


def test_repl_handles_error(tmp_path):
    repl, output = make_repl(tmp_path)

    commands = iter(["unknown", "exit"])
    repl.input_func = lambda prompt: next(commands)

    repl.run()

    assert any("Error:" in x for x in output)


def test_repl_eof(tmp_path):
    repl, output = make_repl(tmp_path)

    def fake_input(prompt):
        raise EOFError

    repl.input_func = fake_input
    repl.run()

    assert output[-1] == "Goodbye!"
