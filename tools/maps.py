import numpy as np


def prorated_map(conc, proxy):
    """
        Creates a prorated map from a binary concordance and proxy vector
    """

    m = conc.shape[1]

    # Input tests
    assert proxy.shape[0] == 1 and proxy.shape[1] == m
    assert np.all((conc == 0) | (conc == 1))

    # Replace very small proxy values
    proxy[proxy < 10**-9] = 10**-8

    # Make the map
    p = proxy[0]
    inner_prod = np.matmul(np.matmul(conc, np.diag(p)), np.ones(m))
    inner_inv = np.linalg.inv(np.diag(inner_prod))
    pro_map = np.matmul(np.matmul(inner_inv, conc), np.diag(p))

    # Tests
    assert np.all(np.isfinite(pro_map))
    assert conc.shape == pro_map.shape
    assert np.all(np.isclose(pro_map.sum(axis=1), 1, atol=10 ** -8))

    return pro_map


