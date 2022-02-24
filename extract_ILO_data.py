import pandas as pd
import os

print('Making Labour satellite')

# Read dataset
data_dir = os.environ['data_dir'] + '/'
df = pd.read_excel(data_dir + 'INJ_FATL_ECO_NB_A_EN.xlsx', skiprows=5)

# Dimensions
years = df['Time'].unique()
countries = df['Reference area'].unique()

print('Dataset contains ' + str(df.shape[0]) + ' records, ' + str(len(years)) + ' years data, ' + str(min(years)) +
      '-' + str(max(years)) + ', ' + str(len(countries)) + ' countries')

