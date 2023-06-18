import pandas as pd


def is_empty(a):

    if a is None:
        return True
    elif isinstance(a, list) or isinstance(a, tuple):
        if len(a) == 0 or a == []:
            return True
        else:
            return False
    elif isinstance(a, dict):
        if a == {}:
            return True
        else:
            return False
    elif isinstance(a, pd.DataFrame):
        if a.shape[0] == 0:
            return True
        else:
            return False
    else:
        raise ValueError('Unknown data type, cannot check emptiness')