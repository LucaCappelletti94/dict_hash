"""Create a dictionary with random values for testing purposes."""

from typing import Dict, Any
import random
import datetime
import re

from random_dict import random_dict
from netaddr import EUI


def create_dict(seed=0) -> Dict[Any, Any]:
    """Create a dictionary with random values for testing purposes."""
    random.seed(seed)
    d = random_dict(random.randint(0, 10), random.randint(0, 10))
    try:
        from numba import typed  # pylint: disable=import-outside-toplevel

        d["numba_list"] = typed.List()
        d["numba_dict"] = typed.Dict()
    except ImportError:
        pass
    d["callable"] = create_dict
    try:
        import numpy as np  # pylint: disable=import-outside-toplevel

        d["numpy"] = np.zeros((10, 10))
        d[tuple((np.str_("ciao"), np.str_("ciao")))] = 9
    except ImportError:
        pass

    d["arbitrary_model"] = EUI("00-1B-77-49-54-FD")
    d["regex"] = re.compile("gugu")

    try:
        import pandas as pd  # pylint: disable=import-outside-toplevel

        d["pandas"] = pd.DataFrame(np.zeros((10, 10)))
        d["pandas_series"] = pd.Series(np.zeros(10))
    except ImportError:
        pass

    try:
        import polars as pl  # pylint: disable=import-outside-toplevel

        d["polars"] = pl.DataFrame(np.ones((10, 10)))
        d["polars_series"] = pl.Series("a", np.ones(10))
    except ImportError:
        pass

    d["date"] = datetime.date(1994, 12, 12)
    d["timedelta"] = datetime.timedelta(days=7)
    d["set"] = {1, 2, 4}
    d["none"] = None
    return d
