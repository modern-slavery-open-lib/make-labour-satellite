import pandas as pd
import os
import tensorflow as tf
import numpy as np

print('Making Labour satellite')

# Disable tensorflow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Paths
data_dir = os.environ['data_dir'] + '/'

# Read dataset
df = pd.read_excel(data_dir + 'INJ_FATL_ECO_NB_A_EN.xlsx', skiprows=5)

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

n_sectors = len(sector_labels)+1  # total value is final sector category

# Check for duplicates
count_recs = df.groupby(['Reference area', 'Time'])['Total'].count().reset_index(name='count')
assert count_recs['count'].max() == 1

# Unpack
subs = []
vals = []
for i, row in df.iterrows():

    v = row['Total']

    if isinstance(v, (int, float, np.number)) and np.isfinite(v) and v > 0:

        t = years.index(row[year_col])
        c = countries.index(row[country_col])

        new_block_subs = [[t, c, n_sectors]]
        new_block_vals = [v]

        for j, s in enumerate(sector_labels):
            sec_val = row[s]
            if isinstance(sec_val, (int, float, np.number)) and np.isfinite(sec_val) and sec_val > 0:
                new_block_subs.append([t, c, j])
                new_block_vals.append(sec_val)

        subs.extend(new_block_subs)
        vals.extend(new_block_vals)

# Tests
assert len(subs) == len(vals)

# Data store
edges = [len(years), len(countries), n_sectors]
store_spten = tf.SparseTensor(indices=subs, values=vals, dense_shape=edges)