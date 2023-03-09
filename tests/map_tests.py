import numpy as np


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
