import csv

import numpy as np
import pandas as pd

from tests.map_tests import conc_is_complete, conc_is_unique, conc_all_is_bool, conc_all_is_numeric


def concordance_reader(fname):

    # Read file
    if fname.endswith('.csv'):
        with open(fname, newline='') as csvfile:
            data = list(csv.reader(csvfile))
        conc = np.array(data, dtype=int)
    elif fname.endswith('.xlsx') or fname.endswith('.xls'):
        conc_df = pd.read_excel(fname, header=0, index_col=0)
        conc = conc_df.values
    else:
        raise ValueError('Unknown file type: ' + fname)

    # Check orientation
    if conc.shape[0] > conc.shape[1]:
        conc = np.transpose(conc)

    return conc


def concordance_test_runner(conc, n_root=6357):

    assert conc.shape[1] == n_root
    assert conc.shape[0] < conc.shape[1]

    conc_all_is_numeric(conc)
    conc_all_is_bool(conc)
    conc_is_unique(conc)
    conc_is_complete(conc)
