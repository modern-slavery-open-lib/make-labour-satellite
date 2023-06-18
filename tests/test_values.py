from lib.configs import get_configs, make_output_dirs
from toolkit.file_io import read_pickle

# Paths
dirs, config = get_configs()
make_output_dirs(dirs)


def test_spotcheck_ilo_inj(publisher='ILO', dataset_id='INJ_FATL_ECO_NB_A_EN'):

    # Read processed data
    data = read_pickle(dirs.processed + publisher + '_' + dataset_id + '.pkl')
    raw_data = data['tensor']
    years = data['years']

    assert raw_data.shape[0] == len(years)
