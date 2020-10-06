import pandas as pd
import numpy as np
import random
from random_dict import random_dict
from numba import typed


def create_dict(seed=0):
    random.seed(seed)
    d = random_dict(random.randint(0, 10), random.randint(0, 10))
    d[tuple((np.str_("ciao"), np.str_("ciao")))] = 9
    d["numba_list"] = typed.List()
    d["numba_dict"] = typed.Dict()
    d["callable"] = create_dict
    d["none"] = None
    return d
