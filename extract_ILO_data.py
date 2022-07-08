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

# Unpack
subs = []
vals = []
for i, row in df.iterrows():

    v = row['Total']

    if isinstance(v, (int, float, np.number)) and np.isfinite(v) and v > 0:
        t = years.index(row[year_col])
        c = countries.index(row[country_col])
        subs.append([t, c])
        vals.append(v)


# Data store
edges = [len(years), len(countries)]
store_spten = tf.SparseTensor(indices=subs, values=vals, dense_shape=edges)