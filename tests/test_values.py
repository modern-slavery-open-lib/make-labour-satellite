import numpy as np

from lib.configs import get_configs
from lib.regions import RootRegions
from toolkit.file_io import read_pickle

# Directories
dirs, _ = get_configs()

# Region definitions
root_regions = RootRegions(conc_dir=dirs.concs)


def test_ilo_inj_meta(publisher='ILO', dataset_id='INJ_FATL_ECO_NB_A_EN'):

    # Read processed data
    data = read_pickle(dirs.processed + publisher + '_' + dataset_id + '.pkl')
    raw_data = data['tensor']
    years = data['years']

    assert raw_data.shape[0] == len(years)
    assert raw_data.shape[1] == root_regions.n_root_regions


def test_ilo_inj_spotcheck(publisher='ILO', dataset_id='INJ_FATL_ECO_NB_A_EN'):

    # Read processed data
    data = read_pickle(dirs.processed + publisher + '_' + dataset_id + '.pkl')
    tensor = data['tensor']

    # Austria, 2018
    year_idx = data['years'].index(2018)
    c_idx = root_regions.find_region_id_from_name('Austria')

    assert np.sum(tensor[year_idx, c_idx-1, :]) == 124

    # USA, 2014
    year_idx = data['years'].index(2014)
    c_idx = root_regions.find_region_id_from_name('USA')

    assert np.sum(tensor[year_idx, c_idx-1, :]) == 4821


def test_ilo_child_meta(publisher='ILO', dataset_id='CLD_XHAZ_SEX_AGE_ECO_NB_A_EN'):

    # Read processed data
    data = read_pickle(dirs.processed + publisher + '_' + dataset_id + '.pkl')
    raw_data = data['tensor']
    years = data['years']

    assert raw_data.shape[0] == len(years)
    assert raw_data.shape[1] == root_regions.n_root_regions


def test_ilo_child_spotcheck(publisher='ILO', dataset_id='CLD_XHAZ_SEX_AGE_ECO_NB_A_EN'):

    # Read processed data
    data = read_pickle(dirs.processed + publisher + '_' + dataset_id + '.pkl')
    tensor = data['tensor']

    # Brazil, 2016
    year_idx = data['years'].index(2016)
    c_idx = root_regions.find_region_id_from_name('Brazil')

    assert np.sum(tensor[year_idx, c_idx-1, :]) == 843.383

    # Sri Lanka, 2016
    year_idx = data['years'].index(2016)
    c_idx = root_regions.find_region_id_from_name('Sri Lanka')

    assert np.isclose(np.sum(tensor[year_idx, c_idx-1, :]), 56.903)


def test_shilling_meta(publisher='JIE', dataset_id='Shilling'):

    # Read processed data
    data = read_pickle(dirs.processed + publisher + '_' + dataset_id + '.pkl')
    raw_data = data['tensor']
    years = data['years']

    assert raw_data.shape[0] == len(years)
    assert raw_data.shape[1] == root_regions.n_root_regions


def test_shilling_spotcheck(publisher='JIE', dataset_id='Shilling'):

    # Read processed data
    data = read_pickle(dirs.processed + publisher + '_' + dataset_id + '.pkl')
    tensor = data['tensor']

    # Brazil, 2016
    year_idx = data['years'].index(2018)
    c_idx = root_regions.find_region_id_from_name('China')

    assert np.isclose(np.sum(tensor[year_idx, c_idx-1, :]), 1932128)

    # Sri Lanka, 2016
    year_idx = data['years'].index(2018)
    c_idx = root_regions.find_region_id_from_name('Egypt')

    assert np.isclose(np.sum(tensor[year_idx, c_idx-1, :]), 143010)


def test_gsi_meta(publisher='GSI', dataset_id='GSI-GEMS'):

    # Read processed data
    data = read_pickle(dirs.processed + publisher + '_' + dataset_id + '.pkl')
    raw_data = data['tensor']
    years = data['years']

    assert raw_data.shape[0] == len(years)
    assert raw_data.shape[1] == root_regions.n_root_regions


def test_gsi_spotcheck(publisher='GSI', dataset_id='GSI-GEMS'):

    # Read processed data
    data = read_pickle(dirs.processed + publisher + '_' + dataset_id + '.pkl')
    tensor = data['tensor']

    # Brazil, 2016
    year_idx = data['years'].index(2023)
    c_idx = root_regions.find_region_id_from_name('Australia')

    assert np.isclose(np.sum(tensor[year_idx, c_idx-1, :]), 41000)

    # Sri Lanka, 2016
    year_idx = data['years'].index(2023)
    c_idx = root_regions.find_region_id_from_name('Vietnam')

    assert np.isclose(np.sum(tensor[year_idx, c_idx-1, :]), 396000)