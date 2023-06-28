import numpy as np
import pandas as pd
from lib.configs import get_configs, make_output_dirs
from lib.preprocessing import concordance_reader, concordance_test_runner
from lib.proxy import retrieve_proxies
from lib.regions import RootRegions
from toolkit.file_io import read_json_from_disk, read_pickle
from toolkit.maps import prorated_map

print('Making Labour satellites...')

# Paths
dirs, config = get_configs()
make_output_dirs(dirs)

# Root definitions
root_regions = RootRegions(conc_dir=dirs.concs)
n_reg_root = root_regions.n_root_regions
n_sec_root = 6357

root_regions = RootRegions(conc_dir=dirs.concs)

# Index of processed data sets
file_index = read_json_from_disk(dirs.object + '/index.json')

# GLORIA regions
reg_root_base_conc = concordance_reader(dirs.concs + config.reg_root_to_base_conc)
n_reg_base = reg_root_base_conc.shape[0]

# Root-to-base concordance
sec_root_base_conc = concordance_reader(dirs.concs + config.sec_root_to_base_conc)
concordance_test_runner(sec_root_base_conc)

n_sec_base = sec_root_base_conc.shape[0]

# Proxies
proxy_dir = dirs.object + '/proxy/'
proxy = retrieve_proxies(n_sec_root, n_reg_root, dirs)

# Add each data source to the satellite
for f in file_index:

    print('Building satellite for ' + f['publisher'] + '-' + f['dataset_id'])

    # Read processed data
    data = read_pickle(dirs.processed + f['publisher'] + '_' + f['dataset_id'] + '.pkl')
    raw_data = data['tensor']
    years = data['years']

    assert raw_data.shape[0] == len(years)

    # Read concordances
    source_root_conc = concordance_reader(dirs.concs + f['concordance_fname'])
    concordance_test_runner(source_root_conc)

    assert source_root_conc.shape[0] == raw_data.shape[2], 'Conc sectoral dim does not match raw data sectoral dim'

    # For each year, map to base sectoral classification and write each base region
    for k, y in enumerate(years):

        satellite = np.array(())

        for r in range(n_reg_base):

            # Find the root countries that are members of this base region
            members = np.where(reg_root_base_conc[r, :] == 1)[0]
            assert len(members) > 0
            base_reg_slice = np.zeros((n_sec_base, ))

            for c in members:

                y_c_slice = raw_data[k, c, :]

                if sum(y_c_slice) > 0:

                    # Transform binary source-to-root conc into a normalised map
                    p = np.expand_dims(proxy[c, :], axis=0)
                    source_root_map = prorated_map(source_root_conc, p)

                    # Make the source to base sectoral map
                    source_base_map = np.matmul(source_root_map, np.transpose(sec_root_base_conc))
                    assert np.all(np.isfinite(source_base_map)), 'Badly formed map'

                    # Apply mapping to raw data
                    y_c_base_slice = np.matmul(y_c_slice, source_base_map)
                    assert np.isclose(sum(y_c_base_slice), sum(y_c_slice), atol=10**-6), 'Map does not preserve total'

                    base_reg_slice = base_reg_slice + y_c_base_slice

            if config.mrio_format == 'IIOT':
                satellite = np.hstack((satellite, base_reg_slice))
            else:
                satellite = np.hstack((np.hstack((np.zeros((n_sec_base,)), satellite)),
                                       base_reg_slice))

        # Tests
        assert np.all(np.isfinite(satellite))
        if config.mrio_format == 'IIOT':
            assert len(satellite) == n_reg_base*n_sec_base
        else:
            assert len(satellite) == n_reg_base * n_sec_base * 2
        assert np.isclose(sum(satellite), sum(sum(raw_data[k, :, :])))

        # Write to disk
        fname = (dirs.satellite + f['publisher'] + '-' + f['dataset_id'] + '-' + config.mrio_format + '-' +
                 'r' + str(n_reg_base) + '-' + 's' + str(n_sec_base) + '-' + str(y) + '.csv')

        pd.DataFrame(np.reshape(satellite, (1, len(satellite)))).to_csv(fname, header=False, index=False)

print('Finished constructing satellites.')
