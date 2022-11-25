import os
import numpy as np
import csv


def retrieve_proxies(n_sec_root, n_reg_root, dirs):
    """
        Reads proxy file is available, other returns a matrix of ones
    """

    proxy_dir = dirs.object + '/proxy/'
    fname = proxy_dir + 'root_proxies_by_country.csv'

    if os.path.isdir(proxy_dir) and os.path.isfile(fname):

        with open(fname, newline='') as csvfile:
            data = list(csv.reader(csvfile))
        proxy = np.array(data, dtype=float)

    else:
        proxy = np.ones((n_reg_root, n_sec_root))

    assert proxy.shape[0] == n_reg_root
    assert proxy.shape[1] == n_sec_root

    return proxy