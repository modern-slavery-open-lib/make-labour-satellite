import math
from numbers import Number
import numpy as np


def is_a_number(x):

    if isinstance(x, Number) and is_finite(x) and not isinstance(x, bool):
        return True
    else:
        return False


def is_finite(x):

    if np.isfinite(x):
        return True
    elif not math.isnan(x) and not np.isnan(x) and not np.isinf(x):
        return True
    else:
        return False


def is_integer(val):

    if isinstance(val, int) or isinstance(val, np.integer):
        return True
    else:
        return False