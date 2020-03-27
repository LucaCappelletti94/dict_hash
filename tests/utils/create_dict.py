from random import seed, randint
import pandas as pd
import numpy as np
from random_dict import random_dict


def create_dict():
    seed(0)
    d = random_dict(randint(0, 10), randint(0, 10))
    d["pandas"] = pd.DataFrame(d)
    d["numpy"] = np.array([1, 2, 3])
    return d
