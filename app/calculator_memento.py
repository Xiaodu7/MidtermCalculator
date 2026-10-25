
from dataclasses import dataclass

from app.calculation import Calculation


@dataclass(frozen=True)
class CalculatorMemento:
    """Save a snapshot of calculator history."""

    calculations: tuple[Calculation, ...]
