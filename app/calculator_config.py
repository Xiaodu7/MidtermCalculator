
import os
import math
import codecs
from pathlib import Path

from dotenv import load_dotenv
from app.exceptions import ValidationError


# Find the main project folder.
BASE_DIR = Path(__file__).resolve().parent.parent


class CalculatorConfig:
    """Load and validate calculator settings."""

    def __init__(self):
        # Read the .env file.
        load_dotenv(BASE_DIR / ".env")

        # Directories
        self.log_dir = self._get_path(
            os.getenv("CALCULATOR_LOG_DIR", "logs")
        )

        self.history_dir = self._get_path(
            os.getenv("CALCULATOR_HISTORY_DIR", "history")
        )

        # File locations
        self.log_file = self._get_path(
            os.getenv(
                "CALCULATOR_LOG_FILE",
                str(self.log_dir / "calculator.log")
            )
        )

        self.history_file = self._get_path(
            os.getenv(
                "CALCULATOR_HISTORY_FILE",
                str(self.history_dir / "calculations.csv")
            )
        )

        # History settings
        self.max_history_size = self._get_int(
            "CALCULATOR_MAX_HISTORY_SIZE", 100
        )

        if self.max_history_size <= 0:
            raise ValidationError(
                "Maximum history size must be positive."
            )

        self.auto_save = self._get_bool(
            "CALCULATOR_AUTO_SAVE", True
        )

        # Calculation settings
        self.precision = self._get_int(
            "CALCULATOR_PRECISION", 6
        )

        if self.precision < 0:
            raise ValidationError(
                "Precision cannot be negative."
            )

        self.max_input_value = self._get_float(
            "CALCULATOR_MAX_INPUT_VALUE", 1000000
        )

        if (
            not math.isfinite(self.max_input_value)
            or self.max_input_value <= 0
        ):
            raise ValidationError(
                "Maximum input value must be positive and finite."
            )

        self.default_encoding = os.getenv(
            "CALCULATOR_DEFAULT_ENCODING", "utf-8"
        )

        try:
            codecs.lookup(self.default_encoding)
        except LookupError as error:
            raise ValidationError(
                "Invalid file encoding."
            ) from error

    @staticmethod
    def _get_path(value):
        """Convert a configured path into an absolute path."""
        path = Path(value).expanduser()

        if not path.is_absolute():
            path = BASE_DIR / path

        return path

    @staticmethod
    def _get_int(name, default):
        """Read an integer setting."""
        try:
            return int(os.getenv(name, default))
        except (ValueError, TypeError) as error:
            raise ValidationError(
                f"{name} must be an integer."
            ) from error

    @staticmethod
    def _get_float(name, default):
        """Read a floating-point setting."""
        try:
            return float(os.getenv(name, default))
        except (ValueError, TypeError) as error:
            raise ValidationError(
                f"{name} must be a number."
            ) from error

    @staticmethod
    def _get_bool(name, default):
        """Read a true/false setting."""
        value = os.getenv(name, str(default)).lower()

        if value == "true":
            return True

        if value == "false":
            return False

        raise ValidationError(
            f"{name} must be true or false."
        )
