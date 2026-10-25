
from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento
from app.exceptions import OperationError, ValidationError


class CalculationHistory:
    """Manage calculation history with undo and redo."""

    def __init__(self, max_size=100):
        if (
            isinstance(max_size, bool)
            or not isinstance(max_size, int)
            or max_size <= 0
        ):
            raise ValidationError(
                "Maximum history size must be a positive integer."
            )

        self.max_size = max_size
        self._calculations = []
        self._undo_stack = []
        self._redo_stack = []

    def _create_memento(self):
        """Save the current history state."""
        return CalculatorMemento(tuple(self._calculations))

    def _restore_memento(self, memento):
        """Restore a previously saved history state."""
        self._calculations = list(memento.calculations)

    def get_history(self):
        """Return a copy of the calculation history."""
        return self._calculations.copy()

    def add(self, calculation):
        """Add a calculation and save the previous state."""
        if not isinstance(calculation, Calculation):
            raise ValidationError("Invalid calculation.")

        self._undo_stack.append(self._create_memento())
        self._redo_stack.clear()

        self._calculations.append(calculation)

        # Keep the history within the allowed size.
        if len(self._calculations) > self.max_size:
            self._calculations.pop(0)

    def clear(self):
        """Clear history while allowing undo."""
        if not self._calculations:
            return

        self._undo_stack.append(self._create_memento())
        self._redo_stack.clear()
        self._calculations.clear()

    def undo(self):
        """Restore the previous history state."""
        if not self._undo_stack:
            raise OperationError("Nothing to undo.")

        self._redo_stack.append(self._create_memento())
        previous_state = self._undo_stack.pop()
        self._restore_memento(previous_state)

    def redo(self):
        """Restore the last undone change."""
        if not self._redo_stack:
            raise OperationError("Nothing to redo.")

        self._undo_stack.append(self._create_memento())
        next_state = self._redo_stack.pop()
        self._restore_memento(next_state)

    def replace(self, calculations):
        """Replace history, for example when loading a CSV."""
        calculations = list(calculations)

        if not all(
            isinstance(item, Calculation)
            for item in calculations
        ):
            raise ValidationError("Invalid history data.")

        self._undo_stack.append(self._create_memento())
        self._redo_stack.clear()
        self._calculations = calculations[-self.max_size:]
