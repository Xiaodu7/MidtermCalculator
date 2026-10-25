
class AutoSaveObserver:
    """Automatically save history after a calculation."""

    def __init__(self, storage):
        self.storage = storage

    def update(self, calculation, history):
        """Save the latest calculation history."""
        self.storage.save(history)
