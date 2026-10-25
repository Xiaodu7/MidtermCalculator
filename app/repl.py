

import sys
from colorama import Fore, Style

from app.calculator import Calculator
from app.calculation import CalculationFactory
from app.exceptions import (
    OperationError,
    ValidationError,
    HistoryError,
)
from app.input_validators import parse_number


class CalculatorREPL:
    """Command-line interface for the calculator."""

    def __init__(
        self,
        calculator=None,
        input_func=input,
        output_func=print
    ):
        self.calculator = (
            calculator if calculator is not None
            else Calculator()
        )
        self.input_func = input_func
        self.output_func = output_func
        
        self.color_enabled = (
            output_func is print and sys.stdout.isatty()
        )


    def display(self, message, color=None):
        """Display a message with optional color."""
        if self.color_enabled and color:
            self.output_func(
                f"{color}{message}{Style.RESET_ALL}"
            )
        else:
            self.output_func(message)


    @staticmethod
    def format_number(number):
        """Display whole numbers without .0."""
        if isinstance(number, float) and number.is_integer():
            return str(int(number))
        return str(number)

    def show_help(self):
        """Display all supported commands."""
        operations = CalculationFactory.OPERATIONS

        self.display("Available operations:", Fore.CYAN)
        self.output_func("  " + ", ".join(operations))

        self.output_func("\nOther commands:")
        self.output_func("  history - Show calculation history")
        self.output_func("  clear   - Clear history")
        self.output_func("  undo    - Undo last change")
        self.output_func("  redo    - Redo last change")
        self.output_func("  save    - Save history to CSV")
        self.output_func("  load    - Load history from CSV")
        self.output_func("  help    - Show this menu")
        self.output_func("  exit    - Exit calculator")

        self.output_func("\nExample: add 5 3")

    def execute(self, line):
        """Execute one user command."""

        parts = line.strip().split()

        if not parts:
            return True

        command = parts[0].lower()
        arguments = parts[1:]

        # Arithmetic operations
        if command in CalculationFactory.OPERATIONS:
            if len(arguments) != 2:
                raise ValidationError(
                    f"Usage: {command} <number1> <number2>"
                )

            a = parse_number(
                arguments[0],
                self.calculator.config.max_input_value
            )
            b = parse_number(
                arguments[1],
                self.calculator.config.max_input_value
            )

            calculation = self.calculator.calculate(
                command, a, b
            )

            
            self.display(
                f"Result: {self.format_number(calculation.result)}",
                Fore.GREEN
            )

            return True

        # Other commands do not need arguments.
        if arguments:
            raise ValidationError(
                f"Command '{command}' does not take arguments."
            )

        if command == "help":
            self.show_help()

        elif command == "history":
            history = self.calculator.get_history()

            if not history:
                self.output_func("History is empty.")
            else:
                for index, calculation in enumerate(
                    history, start=1
                ):
                    a = self.format_number(calculation.a)
                    b = self.format_number(calculation.b)
                    result = self.format_number(
                        calculation.result
                    )

                    self.output_func(
                        f"{index}. {calculation.operation} "
                        f"{a} {b} = {result}"
                    )

        elif command == "clear":
            self.calculator.clear()
            self.display("History cleared.", Fore.YELLOW)

        elif command == "undo":
            self.calculator.undo()
            self.display("Undo successful.", Fore.YELLOW)

        elif command == "redo":
            self.calculator.redo()
            self.display("Redo successful.", Fore.YELLOW)

        elif command == "save":
            path = self.calculator.save()
            self.output_func(
                f"History saved to: {path}"
            )

        elif command == "load":
            history = self.calculator.load()
            self.output_func(
                f"Loaded {len(history)} calculations."
            )

        elif command == "exit":
            self.output_func("Goodbye!")
            return False

        else:
            raise OperationError(
                f"Unknown command: {command}. Type 'help'."
            )

        return True

    def run(self):
        """Start the Read-Eval-Print Loop."""

        self.output_func("Enhanced Calculator")
        self.output_func("Type 'help' for commands.")

        while True:
            try:
                line = self.input_func("Calculator> ")

            except (EOFError, KeyboardInterrupt):
                self.output_func("Goodbye!")
                break

            try:
                should_continue = self.execute(line)

                if not should_continue:
                    break

            except (
                OperationError,
                ValidationError,
                HistoryError,
                OSError,
            ) as error:
                self.display(f"Error: {error}", Fore.RED)
                self.calculator.logger.warning(
                    f"Command error: {error}"
                )
