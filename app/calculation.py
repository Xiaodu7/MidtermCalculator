
from dataclasses import dataclass, field
from datetime import datetime, timezone
import math

from app.operations import Operations
from app.exceptions import OperationError, ValidationError


@dataclass(frozen=True)
class Calculation:
    """Store one calculation and its result."""

    operation: str
    a: float
    b: float
    result: float
    timestamp: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )


class CalculationFactory:
    """Create calculations using the Factory Pattern."""

    OPERATIONS = {
        "add": Operations.add,
        "subtract": Operations.subtract,
        "multiply": Operations.multiply,
        "divide": Operations.divide,
        "power": Operations.power,
        "root": Operations.root,
        "modulus": Operations.modulus,
        "int_divide": Operations.int_divide,
        "percent": Operations.percent,
        "abs_diff": Operations.abs_diff,
    }

    @classmethod
    def create(cls, operation, a, b):
        """Create a calculation from an operation name."""

        # Check the operation name.
        if not isinstance(operation, str):
            raise OperationError("Invalid operation name.")

        operation = operation.strip().lower()

        if operation not in cls.OPERATIONS:
            raise OperationError(
                f"Unknown operation: {operation}"
            )

        # Validate both numbers.
        for number in (a, b):
            if (
                isinstance(number, bool)
                or not isinstance(number, (int, float))
                or not math.isfinite(number)
            ):
                raise ValidationError(
                    "Both inputs must be valid numbers."
                )

        # Perform the selected operation.
        try:
            result = cls.OPERATIONS[operation](a, b)
        except (ZeroDivisionError, ValueError, OverflowError) as error:
            raise OperationError(str(error)) from error

        if isinstance(result, complex) or not math.isfinite(result):
            raise OperationError("Invalid calculation result.")

        # Save the calculation information.
        return Calculation(
            operation=operation,
            a=a,
            b=b,
            result=result
        )
