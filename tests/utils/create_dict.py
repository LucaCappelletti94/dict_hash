import pandas as pd
import numpy as np
import random
from random_dict import random_dict


def create_dict(seed=0):
    random.seed(seed)
    d = random_dict(random.randint(0, 10), random.randint(0, 10))
    d["pandas"] = pd.DataFrame({
        "a": [1, 2, 3]
    })
    d["numpy"] = np.array([1, 2, 3])
    return d
