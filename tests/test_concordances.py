from lib.configs import get_configs
from lib.preprocessing import concordance_reader
from tools.file_io import read_json_from_disk
from tools.maps import conc_all_is_numeric, conc_all_is_bool, conc_is_unique, conc_is_complete

# Directories
dirs, _ = get_configs()

# Index of processed data sets
file_index = read_json_from_disk(dirs.object + '/index.json')

# Constants
n_hscpc = 6357


def test_concordance_shilling(conc_name='shilling_conc.xlsx'):
    conc = concordance_reader(dirs.concs + conc_name)
    conc_all_is_numeric(conc)
    conc_all_is_bool(conc)
    conc_is_unique(conc)
    conc_is_complete(conc)
    assert conc.shape[1] == n_hscpc


def test_concordance_ilo_inj(conc_name='ILO_INJ_FATL_ECO_NB_A_EN_22_conc.xlsx'):
    conc = concordance_reader(dirs.concs + conc_name)
    conc_all_is_numeric(conc)
    conc_all_is_bool(conc)
    conc_is_unique(conc)
    conc_is_complete(conc)
    assert conc.shape[1] == n_hscpc


def test_concordance_ilo_child(conc_name='ILO_CLD_XHAZ_SEX_AGE_ECO_NB_A_EN_3_conc.xlsx'):
    conc = concordance_reader(dirs.concs + conc_name)
    conc_all_is_numeric(conc)
    conc_all_is_bool(conc)
    conc_is_unique(conc)
    conc_is_complete(conc)
    assert conc.shape[1] == n_hscpc