import numpy as np
import pandas as pd
from lib.configs import get_configs, make_output_dirs
from lib.regions import RootRegions


# Paths
dirs, _ = get_configs()
make_output_dirs(dirs)

# Root region definitions
root_regions = RootRegions(conc_dir=dirs.concs)
n_root_regions = root_regions.n_root_regions

# Read datasets
gems_df = pd.read_excel(dirs.raw + 'GEMS.xlsx')
gs_df = pd.read_excel(dirs.raw + '2023-Global-Slavery-Index-Data.xlsx',
                      sheet_name='GSI 2023 summary data', skiprows=2)

# Column indices
country_col = 'Region'
assert country_col in gs_df.columns

# Data dimensions
years = [2022]
countries = list(gs_df[country_col].unique())

n_sectors = 5
n_source_regions = len(countries)
n_years = len(years)

# Unpack
store_tensor = np.zeros((n_years, n_root_regions, n_sectors + 1))
c_root_idx_store = np.zeros((n_source_regions, ), dtype=int)
unmatched = []

