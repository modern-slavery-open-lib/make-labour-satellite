import pandas as pd
import os
import tensorflow as tf
import numpy as np
from tools.file_io import write_pickle
from lib.regions import RootRegions
from tools.sci import is_a_number

print('Unpacking ILO data...')

# Disable tensorflow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Paths
data_dir = os.environ['data_dir'] + '/'
save_dir = os.environ['save_dir'] + '/'

# Root region def
root_regions = RootRegions()
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

# Column indices
country_col = 'Reference area'
assert country_col in df.columns

year_col = 'Time'
assert year_col in df.columns

# Check for duplicates
count_recs = df.groupby(['Reference area', 'Time'])['Total'].count().reset_index()
assert count_recs['Total'].max() == 1, 'Found duplicate records'

# Unpack
subs = []
vals = []
c_root_idx_store = np.zeros((n_source_regions, ))
for i, row in df.iterrows():

    # Year index
    t = years.index(row[year_col])

    # Country index (match source country name to region legend index)
    c_source_name = row[country_col]
    c_source_idx = countries.index(row[country_col])
    if c_root_idx_store[c_source_idx] != 0:
        c_root_id = c_root_idx_store[c_source_idx]
    else:
        c_root_id = root_regions.find_region_id_from_name(c_source_name)
        c_root_idx_store[c_source_idx] = c_root_id

    # Proceed if the country could be matched
    if c_root_id is None:
        print('Skipping ' + c_source_name + '; could not match in root region legend')
    else:
        # Store
        new_block_subs = []
        new_block_vals = []

        # Total value
        v = row['Total']
        if is_a_number(v) and v > 0:
            new_block_subs.append([t, c_source_idx, n_sectors])
            new_block_vals.append(v)

        # Industry values
        for j, s in enumerate(sector_labels):
            sec_val = row[s]
            if is_a_number(sec_val) and sec_val > 0:
                new_block_subs.append([t, c_source_idx, j])
                new_block_vals.append(sec_val)

        # Append to existing store
        if new_block_subs != []:
            subs.extend(new_block_subs)
            vals.extend(new_block_vals)

# Tests
assert len(subs) == len(vals)

print('Unpacked dataset contains ' + str(df.shape[0]) + ' records, ' +
      str(len(years)) + ' years data (' + str(min(years)) + '-' + str(max(years)) + '), ' +
      str(np.where(c_root_idx_store > 0)[0].shape[0]) + ' countries, ' +
      'source industry resolution: ' + str(n_sectors)
      )

# Data store
edges = [len(years), n_root_regions, n_sectors + 1]
store_spten = tf.SparseTensor(indices=subs, values=vals, dense_shape=edges)
store_spten = tf.sparse.reorder(store_spten)

# Save to disk
fname = save_dir + 'ILO_' + ilo_file + '.pkl'
write_pickle(fname, store_spten)

# Dense
ilo_tensor = tf.sparse.to_dense(store_spten)

# Distribution by sectors and country
sector_sum = tf.math.reduce_sum(tf.math.reduce_sum(ilo_tensor, axis=0), axis=0).numpy()
nml_sector_dist = sector_sum[:-1] / np.sum(sector_sum[:-1])

# Make dense copies, by year
# TODO: Describe infilling, here and in README
for i, y in enumerate(years):
    sheet = np.zeros((len(countries), n_sectors))
    for j, c_source_idx in enumerate(countries):
        slice_yc = ilo_tensor[i, j, :].numpy()
        total = slice_yc[-1]
        if sum(slice_yc) > 0:
            ind_vals = slice_yc[:-1]
            if np.sum(ind_vals) >= total:
                sheet[j, :] = ind_vals
            elif np.sum(ind_vals) == 0 and total > 0:
                sheet[j, :] = total*nml_sector_dist
            else:
                scaler = total/np.sum(ind_vals)
                sheet[j, :] = ind_vals * scaler

            assert all(np.isfinite(sheet[j, :])) and np.sum(sheet[j, :]) > 0

    # Write to disk
    fname = save_dir + 'ILO_fatalities_' + str(y) + '.xlsx'
    df = pd.DataFrame(sheet, columns=sector_labels)
    df['countries'] = countries
    df.set_index('countries').to_excel(fname)