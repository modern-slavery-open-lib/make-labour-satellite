import pandas as pd
import os
import tensorflow as tf
import numpy as np
from utils import write_pickle


print('Making Labour satellite')

# Disable tensorflow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Paths
data_dir = os.environ['data_dir'] + '/'
save_dir = os.environ['save_dir'] + '/'

# Read dataset
ilo_file = 'INJ_FATL_ECO_NB_A_EN'
df = pd.read_excel(data_dir + ilo_file + '.xlsx', skiprows=5)

# Dimensions
years = list(df['Time'].unique())
countries = list(df['Reference area'].unique())
sector_labels = df.columns[4:-1].to_list()

print('Dataset contains ' + str(df.shape[0]) + ' records, ' +
      str(len(years)) + ' years data, ' + str(min(years)) + '-' + str(max(years)) + ', ' +
      str(len(countries)) + ' countries')

# Column indices
country_col = 'Reference area'
assert country_col in df.columns

year_col = 'Time'
assert year_col in df.columns

n_sectors = len(sector_labels)  # total value is final sector category

# Check for duplicates
count_recs = df.groupby(['Reference area', 'Time'])['Total'].count().reset_index(name='count')
assert count_recs['count'].max() == 1

# Unpack
subs = []
vals = []
for i, row in df.iterrows():

    # Meta
    t = years.index(row[year_col])
    c = countries.index(row[country_col])

    # Store
    new_block_subs = []
    new_block_vals = []

    # Total value
    v = row['Total']
    if isinstance(v, (int, float, np.number)) and np.isfinite(v) and v > 0:
        new_block_subs.append([t, c, n_sectors])
        new_block_vals.append(v)

    # Industry values
    for j, s in enumerate(sector_labels):
        sec_val = row[s]
        if isinstance(sec_val, (int, float, np.number)) and np.isfinite(sec_val) and sec_val > 0:
            new_block_subs.append([t, c, j])
            new_block_vals.append(sec_val)

    # Append to existing store
    if new_block_subs != []:
        subs.extend(new_block_subs)
        vals.extend(new_block_vals)

# Tests
assert len(subs) == len(vals)

# Data store
edges = [len(years), len(countries), n_sectors+1]
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
for i, y in enumerate(years):
    sheet = np.zeros((len(countries), n_sectors))
    for j, c in enumerate(countries):
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