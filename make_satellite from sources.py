from pathlib import Path
from lib.preprocessing import concordance_reader, concordance_test_runner
from lib.regions import RootRegions
from tools.file_io import read_json_from_disk, read_pickle
import numpy as np

print('Making Labour satellite')

# Paths
current_working_dir = str(Path.cwd())
object_dir = current_working_dir + '/objects/'

# Index of processed data sets
file_index = read_json_from_disk(object_dir + '/index.json')

# Root region definitions
root_regions = RootRegions(object_dir=object_dir)

# Root-to-base concordance
root_base_conc = concordance_reader(object_dir + '/concs/HSCPC_Eora25_secagg.csv')
concordance_test_runner(root_base_conc)

for f in file_index:

    print('Building satellite for ' + f['publisher'] + '-' + f['dataset_id'])

    # Read processed data
    data = read_pickle(object_dir + '/processed/' + f['processed_fname'])

    # Read concordances
    source_root_conc = concordance_reader(object_dir + '/concs/' + f['concordance_fname'])
    concordance_test_runner(source_root_conc)

    a=1
    #source_base_map = np.matmul(source_root_map, np.transpose(root_base_map))