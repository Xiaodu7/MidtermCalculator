
import json
import math
from datetime import datetime
from pathlib import Path

import pandas as pd

from app.calculation import Calculation, CalculationFactory
from app.exceptions import HistoryError


class HistoryStorage:
    """Save and load calculation history using pandas."""

    COLUMNS = [
        "operation",
        "operands",
        "result",
        "timestamp",
    ]

    def __init__(self, config):
        self.path = Path(config.history_file)
        self.encoding = config.default_encoding

    def save(self, calculations):
        """Save calculations to a CSV file."""
        rows = []

        for calculation in calculations:
            if not isinstance(calculation, Calculation):
                raise HistoryError("Invalid calculation in history.")

            rows.append({
                "operation": calculation.operation,
                "operands": json.dumps([
                    calculation.a,
                    calculation.b
                ]),
                "result": calculation.result,
                "timestamp": calculation.timestamp,
            })

        try:
            self.path.parent.mkdir(
                parents=True, exist_ok=True
            )

            dataframe = pd.DataFrame(
                rows, columns=self.COLUMNS
            )

            dataframe.to_csv(
                self.path,
                index=False,
                encoding=self.encoding
            )

        except (OSError, ValueError, TypeError) as error:
            raise HistoryError(
                f"Could not save history: {error}"
            ) from error

        return self.path

    def load(self):
        """Load calculations from a CSV file."""
        if not self.path.is_file():
            raise HistoryError(
                f"History file does not exist: {self.path}"
            )

        try:
            dataframe = pd.read_csv(
                self.path,
                encoding=self.encoding
            )

        except (
            OSError,
            ValueError,
            UnicodeError,
        ) as error:
            raise HistoryError(
                f"Could not read history: {error}"
            ) from error

        if not set(self.COLUMNS).issubset(dataframe.columns):
            raise HistoryError(
                "History CSV has missing columns."
            )

        calculations = []

        for index, row in dataframe.iterrows():
            try:
                operation = row["operation"]

                if operation not in CalculationFactory.OPERATIONS:
                    raise ValueError("Unknown operation.")

                operands = json.loads(row["operands"])

                if (
                    not isinstance(operands, list)
                    or len(operands) != 2
                    or any(
                        type(value) not in (int, float)
                        or not math.isfinite(value)
                        for value in operands
                    )
                ):
                    raise ValueError("Invalid operands.")

                result = float(row["result"])

                if not math.isfinite(result):
                    raise ValueError("Invalid result.")

                timestamp = str(row["timestamp"])
                datetime.fromisoformat(timestamp)

                calculations.append(
                    Calculation(
                        operation=operation,
                        a=operands[0],
                        b=operands[1],
                        result=result,
                        timestamp=timestamp
                    )
                )

            except (
                ValueError,
                TypeError,
                OverflowError,
            ) as error:
                raise HistoryError(
                    f"Invalid history row {index + 2}: {error}"
                ) from error

        return calculations
