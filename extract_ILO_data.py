import os
import numpy as np
import pandas as pd
from pathlib import Path
from lib.regions import RootRegions
from tools.file_io import write_pickle
from tools.sci import is_a_number
import re

print('Unpacking ILO data...')

# Settings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Disable tensorflow logging
infill_missing = True

# Paths
current_working_dir = str(Path.cwd())
root_dir = re.match("(.*make-labour-satellite)", current_working_dir).group(1)
data_dir = root_dir + '/objects/raw/'
save_dir = root_dir + '/objects/processed/'

# Root region definitions
root_regions = RootRegions(object_dir=root_dir + '/objects/')
n_root_regions = root_regions.n_root_regions

# Read dataset
ilo_file = 'INJ_FATL_ECO_NB_A_EN'
df = pd.read_excel(data_dir + ilo_file + '.xlsx', skiprows=5)

# Data dimensions
years = list(df['Time'].unique())
countries = list(df['Reference area'].unique())
sector_labels = df.columns[4:-1].to_list()

n_sectors = len(sector_labels)  # source sectors, total value is final sector category
n_source_regions = len(countries)
n_years = len(years)

# Column indices
country_col = 'Reference area'
assert country_col in df.columns

year_col = 'Time'
assert year_col in df.columns

# Check for duplicates
count_recs = df.groupby(['Reference area', 'Time'])['Total'].count().reset_index()
assert count_recs['Total'].max() == 1, 'Found duplicate records'

# Unpack
store_tensor = np.zeros((n_years, n_root_regions, n_sectors + 1))
c_root_idx_store = np.zeros((n_source_regions, ), dtype=int)

for i, row in df.iterrows():

    # Year index
    t = years.index(row[year_col]) - 1

    # Country index (match source country name to region legend index)
    c_source_name = row[country_col]
    c_source_idx = countries.index(row[country_col])
    if c_root_idx_store[c_source_idx] != 0:
        c_root_idx = int(c_root_idx_store[c_source_idx])
    else:
        c_root_idx = root_regions.find_region_id_from_name(c_source_name)
        if c_root_idx is not None:
            assert c_root_idx_store[c_source_idx] == 0
            c_root_idx_store[c_source_idx] = c_root_idx

    # Proceed if the country could be matched
    if c_root_idx is None:
        print('Skipping ' + c_source_name + '; could not match in root region legend')
    else:
        c_root_idx = c_root_idx - 1

        # Total value
        v = row['Total']
        if is_a_number(v) and v > 0:
            store_tensor[t, c_root_idx, n_sectors] = v

        # Industry values
        for j, s in enumerate(sector_labels):
            sec_val = row[s]
            if is_a_number(sec_val) and sec_val > 0:
                store_tensor[t-1, c_root_idx-1, j] = sec_val

# Tests
assert np.all(np.isfinite(store_tensor)) and np.all(store_tensor >= 0)

print('Unpacked dataset contains ' + str(df.shape[0]) + ' records, ' +
      str(len(years)) + ' years data (' + str(min(years)) + '-' + str(max(years)) + '), ' +
      str(np.where(c_root_idx_store > 0)[0].shape[0]) + ' countries, ' +
      'source industry resolution: ' + str(n_sectors)
      )

# Perform infilling
if infill_missing:

    # Distribution by sectors and country
    sector_sum = store_tensor.sum(axis=0).sum(axis=0)
    nml_sector_dist = sector_sum[:-1] / np.sum(sector_sum[:-1])

    # Perform infilling, where total exist, infer sector distribution
    for y in range(n_years-1):
        for c in range(n_root_regions-1):
            if store_tensor[y, c, :].sum() > 0:
                total = store_tensor[y, c, -1]
                ind_vals = store_tensor[y, c, :-1]
                if np.sum(ind_vals) >= total:
                    store_tensor[y, c, :-1] = ind_vals
                elif np.sum(ind_vals) == 0 and total > 0:
                    store_tensor[y, c, :-1] = total*nml_sector_dist
                else:
                    scaler = total/np.sum(ind_vals)
                    store_tensor[y, c, :-1] = ind_vals * scaler

# Tests
assert np.all(np.isfinite(store_tensor)) and np.all(store_tensor >= 0)

# Drop totals
store_tensor = store_tensor[:, :, :-1]

# Make data store
store = {"edges": [len(years), n_root_regions, n_sectors],
         "tensor": store_tensor,
         "years": years
         }

# Save to disk
fname = save_dir + 'ILO_' + ilo_file + '.pkl'
write_pickle(fname, store)