from pathlib import Path
from lib.preprocessing import concordance_reader, concordance_test_runner
from lib.regions import RootRegions
from tools.file_io import read_json_from_disk, read_pickle
from tools.maps import create_prorated_map
import numpy as np
import os

print('Making Labour satellite')

# Paths
current_working_dir = str(Path.cwd())
object_dir = current_working_dir + '/objects/'

# Index of processed data sets
file_index = read_json_from_disk(object_dir + '/index.json')

# Root region definitions
root_regions = RootRegions(object_dir=object_dir)

# GLORIA regions
reg_root_base_conc = concordance_reader(object_dir + '/concs/UNEP_IRP_164RegAgg.csv')
n_reg_gloria = reg_root_base_conc.shape[0]

# Root-to-base concordance
sec_root_base_conc = concordance_reader(object_dir + '/concs/HSCPC_Eora25_secagg.csv')
concordance_test_runner(sec_root_base_conc)

# Proxies
proxy_dir = object_dir + '/proxy/'
if os.path.isdir(proxy_dir):
    proxy = np.ones((221, 6357))
else:
    proxy = np.ones((221, 6357))

# Add each data source to the satellite
for f in file_index:

    print('Building satellite for ' + f['publisher'] + '-' + f['dataset_id'])

    # Read processed data
    data = read_pickle(object_dir + '/processed/' + f['processed_fname'])

    # Read concordances
    source_root_conc = concordance_reader(object_dir + '/concs/' + f['concordance_fname'])
    concordance_test_runner(source_root_conc)

    satellite = np.array(())

    # Make maps
    for r in range(n_reg_gloria):
        members = np.where(reg_root_base_conc[r, :] == 1)[0]
        for s in members:

            p = np.expand_dims(proxy[s, :], axis=0)
            source_root_map = create_prorated_map(source_root_conc, p)
            root_base_map = create_prorated_map(sec_root_base_conc, p)

            source_base_map = np.matmul(source_root_map, np.transpose(root_base_map))
            assert np.all(np.isfinite(source_base_map))

            stop = 1