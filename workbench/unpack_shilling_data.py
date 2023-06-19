import numpy as np
import pandas as pd
from lib.configs import get_configs, make_output_dirs
from lib.regions import RootRegions
from toolkit.file_io import write_pickle

# Paths
dirs, _ = get_configs()
make_output_dirs(dirs)

# Root region definitions
root_regions = RootRegions(conc_dir=dirs.concs)
n_root_regions = root_regions.n_root_regions

# Read dataset
data_file = 'Shilling_Matrix_GTAP-AgUnSk'
df = pd.read_excel(dirs.raw + data_file + '.xlsx', header=0)

# Column indices
country_col = 'Description (County or Region)'
assert country_col in df.columns

# Data dimensions
years = [2018]
countries = list(df[country_col].unique())
sector_labels = df.columns[4:].to_list()

n_sectors = len(sector_labels)  # source sectors, total value is final sector category
n_source_regions = len(countries)
n_years = 1

# Unpack
store_tensor = np.zeros((n_years, n_root_regions, n_sectors))

for i, row in df.iterrows():

    # Country index (match source country name to region legend index)
    c_source_name = row[country_col]
    c_root_idx = root_regions.find_region_id_from_name(c_source_name)

    # Proceed if the country could be matched
    if c_root_idx is None:
        print('Skipping ' + c_source_name + '; could not match in root region legend')
    else:
        c_root_idx = c_root_idx - 1
        vals = row[4:].values
        vals_fl = np.array(list(vals), dtype=float)
        store_tensor[0, c_root_idx, :] = vals_fl

# Tests
assert np.all(np.isfinite(store_tensor)) and np.all(store_tensor >= 0)

# Make data store
store = {"edges": [len(years), n_root_regions, n_sectors],
         "tensor": store_tensor,
         "years": years
         }

# Save to disk
fname = dirs.processed + 'JIE_' + 'Shilling' + '.pkl'
write_pickle(fname, store)

# Logging
n_countries_data = len(np.where(np.sum(np.sum(store_tensor, axis=2), axis=0) > 0)[0])
print('Unpacked dataset contains ' + str(df.shape[0]) + ' records, ' +
      str(len(years)) + ' year(s) data (' + str(min(years)) + '-' + str(max(years)) + '), ' +
      str(n_countries_data) + ' countries, ' +
      'source industry resolution: ' + str(n_sectors)
      )
