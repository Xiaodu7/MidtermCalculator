
import math

from app.exceptions import ValidationError


def parse_number(value, max_input_value):
    """Convert user input into a valid number."""

    try:
        number = float(value)
    except (ValueError, TypeError) as error:
        raise ValidationError(
            f"Invalid number: {value}"
        ) from error

    if not math.isfinite(number):
        raise ValidationError(
            "Input must be a finite number."
        )

    if abs(number) > max_input_value:
        raise ValidationError(
            "Input exceeds maximum allowed value."
        )

    return number
