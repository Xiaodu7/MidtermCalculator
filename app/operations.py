
import math


class Operations:
    """Basic and advanced calculator operations."""

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b

    @staticmethod
    def power(a, b):
        if a < 0 and not float(b).is_integer():
            raise ValueError("Result is not a real number.")
        return a ** b

    @staticmethod
    def root(a, b):
        if b == 0:
            raise ValueError("Root degree cannot be zero.")

        if a == 0 and b < 0:
            raise ZeroDivisionError("Cannot divide by zero.")

        if a < 0:
            if not float(b).is_integer() or int(b) % 2 == 0:
                raise ValueError("Invalid root of a negative number.")
            return -((-a) ** (1 / b))

        return a ** (1 / b)

    @staticmethod
    def modulus(a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a % b

    @staticmethod
    def int_divide(a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return math.trunc(a / b)

    @staticmethod
    def percent(a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return (a / b) * 100

    @staticmethod
    def abs_diff(a, b):
        return abs(a - b)
