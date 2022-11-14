import csv
import numpy as np
from tests.map_tests import conc_is_complete, conc_is_unique, conc_all_is_bool, conc_all_is_numeric


def read_aggregator(fname, n_root=6357):

    # Read file
    with open(fname, newline='') as csvfile:
        data = list(csv.reader(csvfile))
    conc = np.array(data, dtype=int)

    # Check orientation
    if conc.shape[0] > conc.shape[1]:
        conc = np.transpose(conc)

    assert conc.shape[1] == n_root

    # Perform tests
    conc_all_is_numeric(conc)
    conc_all_is_bool(conc)
    conc_is_unique(conc)
    conc_is_complete(conc)

    return conc