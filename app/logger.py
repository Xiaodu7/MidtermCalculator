
import logging
from pathlib import Path


class Logger:
    """Manage logging for the calculator."""

    def __init__(self, config):
        self.config = config

        # Get the log file path from configuration.
        self.log_file = Path(config.log_file)
        self.log_file.parent.mkdir(
            parents=True, exist_ok=True
        )

        # Create a logger for this file.
        self.logger = logging.getLogger(
            f"calculator.{self.log_file.resolve()}"
        )
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        # Avoid adding duplicate file handlers.
        if not self.logger.handlers:
            handler = logging.FileHandler(
                self.log_file,
                encoding=config.default_encoding
            )

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s"
            )

            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message):
        """Log general information."""
        self.logger.info(message)

    def warning(self, message):
        """Log a warning."""
        self.logger.warning(message)

    def error(self, message):
        """Log an error."""
        self.logger.error(message)

    def log_calculation(self, calculation):
        """Log the details of a calculation."""
        message = (
            f"Operation: {calculation.operation}, "
            f"Operands: {calculation.a}, {calculation.b}, "
            f"Result: {calculation.result}, "
            f"Timestamp: {calculation.timestamp}"
        )

        self.info(message)


class LoggingObserver:
    """Log calculations when notified by the calculator."""

    def __init__(self, logger):
        self.logger = logger

    def update(self, calculation, history=None):
        """Respond to a new calculation."""
        self.logger.log_calculation(calculation)
