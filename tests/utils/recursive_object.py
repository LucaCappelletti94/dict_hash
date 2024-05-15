"""Recursive object for testing purposes."""


class RecursiveObject:
    """Recursive object for testing purposes."""

    recursive_attribute = None

    def __init__(self):
        self.recursive_attribute = self
