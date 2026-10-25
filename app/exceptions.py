
class OperationError(Exception):
    """Error related to calculator operations."""
    pass


class ValidationError(Exception):
    """Error related to invalid user input."""
    pass


class HistoryError(Exception):
    """Error when saving or loading calculation history."""
    pass
