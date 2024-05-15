"""Submodule providing a class that is not hashable."""
import polars as pl


class NotHashable:
    """Class that is not hashable."""

    not_hashable_attribute = pl.DataFrame()
