"""Create a dictionary with random values for testing purposes."""
from typing import Dict, Any
import random
from datetime import date

import numpy as np
import pandas as pd
from numba import typed
import re
from random_dict import random_dict
from netaddr import EUI


def create_dict(seed=0) -> Dict[Any, Any]:
    """Create a dictionary with random values for testing purposes."""
    random.seed(seed)
    d = random_dict(random.randint(0, 10), random.randint(0, 10))
    d[tuple((np.str_("ciao"), np.str_("ciao")))] = 9
    d["numba_list"] = typed.List()
    d["numba_dict"] = typed.Dict()
    d["callable"] = create_dict
    d["numpy"] = np.zeros((100, 100))
    d["arbitrary_model"] = EUI("00-1B-77-49-54-FD")
    d["regex"] = re.compile("gugu")
    d["pandas"] = pd.DataFrame(np.zeros((100, 100)))
    d["date"] = date(1994, 12, 12)
    d["set"] = {1, 2, 4}
    d["none"] = None
    return d
