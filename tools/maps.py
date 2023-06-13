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


def conc_all_is_numeric(ar):
    assert np.all(np.isfinite(ar))


def conc_all_is_bool(ar):
    assert ((ar == 0) | (ar == 1)).all()


def conc_is_unique(ar):
    marginal_sum = ar.sum(axis=0)
    assert np.all(marginal_sum == 1), 'Concordances is not unique, root should be mapped to only one base sector'


def conc_is_complete(ar):
    marginal_sum = ar.sum(axis=1)
    assert np.all(marginal_sum > 0), 'Concordances is not complete, source should be mapped to at least one root sector'
