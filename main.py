
from app.repl import CalculatorREPL
from app.exceptions import ValidationError


def main():
    """Start the calculator application."""
    try:
        calculator_repl = CalculatorREPL()
        calculator_repl.run()
    except (ValidationError, OSError) as error:
        print(f"Startup error: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
