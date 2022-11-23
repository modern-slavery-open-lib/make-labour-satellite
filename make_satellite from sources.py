import os
import numpy as np
import pandas as pd
from lib.configs import get_configs, make_output_dirs
from lib.preprocessing import concordance_reader, concordance_test_runner
from lib.regions import RootRegions
from tools.file_io import read_json_from_disk, read_pickle
from tools.maps import prorated_map

print('Making Labour satellite')

# Paths
dirs = get_configs()
make_output_dirs(dirs)

# Index of processed data sets
file_index = read_json_from_disk(dirs.object + '/index.json')

# Root region definitions
root_regions = RootRegions(object_dir=dirs.object)

# GLORIA regions
reg_root_base_conc = concordance_reader(dirs.concs + 'UNEP_IRP_164RegAgg.csv')
n_reg_base = reg_root_base_conc.shape[0]

# Root-to-base concordance
sec_root_base_conc = concordance_reader(dirs.concs + 'HSCPC_Eora25_secagg.csv')
concordance_test_runner(sec_root_base_conc)

n_sec_base = sec_root_base_conc.shape[0]

# Proxies
proxy_dir = dirs.object + '/proxy/'
if os.path.isdir(proxy_dir):
    proxy = np.ones((221, 6357))
else:
    proxy = np.ones((221, 6357))

# Add each data source to the satellite
for f in file_index:

    print('Building satellite for ' + f['publisher'] + '-' + f['dataset_id'])

    # Read processed data
    data = read_pickle(dirs.processed + f['processed_fname'])
    raw_data = data['tensor']
    years = data['years']

    assert raw_data.shape[0] == len(years)

    # Read concordances
    source_root_conc = concordance_reader(dirs.concs + f['concordance_fname'])
    concordance_test_runner(source_root_conc)

    assert source_root_conc.shape[0] == raw_data.shape[2], 'Conc sectoral dim does not match raw data sectoral dim'

    # Make maps
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

                    # Make the source to base sectoral map
                    p = np.expand_dims(proxy[c, :], axis=0)
                    source_root_map = prorated_map(source_root_conc, p)

                    source_base_map = np.matmul(source_root_map, np.transpose(sec_root_base_conc))
                    assert np.all(np.isfinite(source_base_map)), 'Badly formed map'

                    # Apply mapping to raw data
                    y_c_base_slice = np.matmul(y_c_slice, source_base_map)
                    assert np.isclose(sum(y_c_base_slice), sum(y_c_slice), atol=10**-6), 'Map does not preserve total'

                    base_reg_slice = base_reg_slice + y_c_base_slice

            satellite = np.hstack((satellite, base_reg_slice))

        # Tests
        assert len(satellite) == n_reg_base*n_sec_base
        assert np.isclose(sum(satellite), sum(sum(raw_data[k, :, :])))

        # Write to disk
        fname = dirs.satellite + f['publisher'] + '-' + f['dataset_id'] + '-' + str(y) + '.csv'
        pd.DataFrame(np.reshape(satellite, (1, len(satellite)))).to_csv(fname, header=False, index=False)