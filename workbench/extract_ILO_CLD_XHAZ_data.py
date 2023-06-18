import numpy as np
import pandas as pd

from lib.configs import get_configs, make_output_dirs
from lib.regions import RootRegions
from toolkit.dict import match_key_in_dlist
from toolkit.file_io import write_pickle, read_json_from_disk
from toolkit.sci import is_a_number
from toolkit.sets import is_empty

print('Unpacking ILO data...')

# Settings
dataset_id = 'CLD_XHAZ_SEX_AGE_ECO_NB_A_EN'

# Paths
dirs, _ = get_configs()
make_output_dirs(dirs)

# Root region definitions
root_regions = RootRegions(conc_dir=dirs.concs)
n_root_regions = root_regions.n_root_regions

# Index of processed data sets
file_index = read_json_from_disk(dirs.object + '/index.json')
index_rec = match_key_in_dlist(file_index, 'dataset_id', dataset_id)
assert not is_empty(index_rec)

if 'fill_missing_from_totals' in index_rec[0] and index_rec[0]['fill_missing_from_totals'] is True:
    infill_missing = True
else:
    infill_missing = False

# Read dataset
df = pd.read_excel(dirs.raw + dataset_id + '.xlsx', skiprows=5)

# Column indices
country_col = 'Reference area'
assert country_col in df.columns

# Data dimensions
years = list(np.sort(df['Time'].unique()))
countries = list(df[country_col].unique())
sector_labels = df.columns[6:-2].to_list()

n_sectors = len(sector_labels)  # source sectors, total value is final sector category
n_source_regions = len(countries)
n_years = len(years)

year_col = 'Time'
assert year_col in df.columns

# Unpack
store_tensor = np.zeros((n_years, n_root_regions, n_sectors + 1))
c_root_idx_store = np.zeros((n_source_regions, ), dtype=int)
unmatched = []

for i, row in df.iterrows():

    # Year index
    t = years.index(row[year_col])

    # Country index (match source country name to region legend index)
    c_source_name = row[country_col]
    c_source_idx = countries.index(c_source_name)
    if c_root_idx_store[c_source_idx] != 0:
        c_root_idx = int(c_root_idx_store[c_source_idx])
    else:
        c_root_idx = root_regions.find_region_id_from_name(c_source_name)
        if c_root_idx is not None:
            assert c_root_idx_store[c_source_idx] == 0
            c_root_idx_store[c_source_idx] = c_root_idx

    # Proceed if the country could be matched
    if c_root_idx is None:
        if c_source_name not in unmatched:
            unmatched.append(c_source_name)

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
                store_tensor[t, c_root_idx, j] = sec_val

# Tests
assert np.all(np.isfinite(store_tensor)) and np.all(store_tensor >= 0)

# Logging
print('Skipped ' + str(len(unmatched)) + ' unmatched regions: ' + ', '.join(unmatched))

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
    for y in range(n_years):
        for c in range(n_root_regions):
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
fname = dirs.processed + 'ILO_' + dataset_id + '.pkl'
write_pickle(fname, store)
