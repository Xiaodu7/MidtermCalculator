
import math
from dataclasses import replace

from app.calculation import CalculationFactory
from app.calculator_config import CalculatorConfig
from app.exceptions import (
    HistoryError,
    OperationError,
    ValidationError,
)
from app.history import CalculationHistory
from app.history_storage import HistoryStorage
from app.logger import Logger, LoggingObserver
from app.observers import AutoSaveObserver


class Calculator:
    """Main calculator class connecting all components."""

    def __init__(self, config=None):
        self.config = (
            config if config is not None
            else CalculatorConfig()
        )

        # Create history, storage, and logger.
        self.history = CalculationHistory(
            self.config.max_history_size
        )
        self.storage = HistoryStorage(self.config)
        self.logger = Logger(self.config)

        # Register observers.
        self._observers = []
        self.register_observer(
            LoggingObserver(self.logger)
        )

        if self.config.auto_save:
            self.register_observer(
                AutoSaveObserver(self.storage)
            )

        self.logger.info("Calculator initialized.")

    def register_observer(self, observer):
        """Register an observer for new calculations."""
        if not callable(getattr(observer, "update", None)):
            raise ValidationError("Invalid observer.")

        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        """Remove an existing observer."""
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(self, calculation):
        """Notify observers about a new calculation."""
        for observer in tuple(self._observers):
            observer.update(
                calculation,
                self.history.get_history()
            )

    def calculate(self, operation, a, b):
        """Perform a calculation and update history."""

        try:
            # Validate input numbers and their range.
            for value in (a, b):
                if (
                    isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or not math.isfinite(value)
                ):
                    raise ValidationError(
                        "Both inputs must be valid numbers."
                    )

                if abs(value) > self.config.max_input_value:
                    raise ValidationError(
                        "Input exceeds maximum allowed value."
                    )

            # Use Factory Pattern to create calculation.
            calculation = CalculationFactory.create(
                operation, a, b
            )

            # Apply configured result precision.
            calculation = replace(
                calculation,
                result=round(
                    calculation.result,
                    self.config.precision
                )
            )

            # Update history.
            self.history.add(calculation)

            # Notify LoggingObserver and AutoSaveObserver.
            self._notify_observers(calculation)

            return calculation

        except (ValidationError, OperationError) as error:
            self.logger.warning(
                f"Calculation rejected: {error}"
            )
            raise

        except (HistoryError, OSError) as error:
            self.logger.error(
                f"Calculation storage failed: {error}"
            )
            raise

    def get_history(self):
        """Return the current calculation history."""
        return self.history.get_history()

    def _sync_history(self):
        """Keep saved history updated after changes."""
        if self.config.auto_save:
            self.save()

    def clear(self):
        """Clear calculation history."""
        self.history.clear()
        self._sync_history()
        self.logger.info("History cleared.")

    def undo(self):
        """Undo the most recent history change."""
        self.history.undo()
        self._sync_history()
        self.logger.info("Undo performed.")

    def redo(self):
        """Redo the previously undone change."""
        self.history.redo()
        self._sync_history()
        self.logger.info("Redo performed.")

    def save(self):
        """Manually save history to CSV."""
        path = self.storage.save(
            self.history.get_history()
        )
        self.logger.info(f"History saved to {path}")
        return path

    def load(self):
        """Load saved history from CSV."""
        calculations = self.storage.load()
        self.history.replace(calculations)

        self.logger.info("History loaded from CSV.")
        return self.history.get_history()
