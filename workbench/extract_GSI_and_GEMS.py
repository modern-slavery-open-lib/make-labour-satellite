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

# Read datasets
gems_df = pd.read_excel(dirs.raw + 'GEMS.xlsx')
gs_df = pd.read_excel(dirs.raw + '2023-Global-Slavery-Index-Data.xlsx', sheet_name='GSI 2023 summary data', skiprows=2)

# GEMS proxy
gems_proxy = gems_df['Forced labour'].values / gems_df['Forced labour'].sum()

# Column indices
country_col = 'Country'
assert country_col in gs_df.columns

value_col = 'Estimated number of people in modern slavery'
assert value_col in gs_df.columns

# Data dimensions
years = [2022]
countries = list(gs_df[country_col].unique())

n_sectors = gems_df.shape[0]
n_source_regions = len(countries)
n_years = len(years)

# Unpack
store_tensor = np.zeros((n_years, n_root_regions, n_sectors))
c_root_idx_store = np.zeros((n_source_regions, ), dtype=int)

for i, row in gs_df.iterrows():

    # Country index (match source country name to region legend index)
    c_source_name = row[country_col]
    c_root_idx = root_regions.find_region_id_from_name(c_source_name)

    # Proceed if the country could be matched
    if c_root_idx is None:
        print('Skipping ' + c_source_name + '; could not match in root region legend')
    else:

        # Extract value
        val = row.to_dict()[value_col]

        if np.isfinite(val):

            # Disaggregate using GEMS
            vec = val * gems_proxy

            # Write to store
            store_tensor[0, c_root_idx - 1, :] = vec

# Tests
assert np.all(np.isfinite(store_tensor)) and np.all(store_tensor >= 0)

# Make data store
store = {"edges": [len(years), n_root_regions, n_sectors],
         "tensor": store_tensor,
         "years": years
         }

# Save to disk
fname = dirs.processed + 'GSI_' + 'GSI-GEMS' + '.pkl'
write_pickle(fname, store)

# Logging
n_countries_data = len(np.where(np.sum(np.sum(store_tensor, axis=2), axis=0) > 0)[0])
print('Unpacked dataset contains ' + str(gs_df.shape[0]) + ' records, ' +
      str(len(years)) + ' year(s) data (' + str(min(years)) + '-' + str(max(years)) + '), ' +
      str(n_countries_data) + ' countries, ' +
      'source industry resolution: ' + str(n_sectors)
      )

