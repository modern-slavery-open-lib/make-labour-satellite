import numpy as np
import pandas as pd
from lib.configs import get_configs, make_output_dirs
from lib.regions import RootRegions
from tools.file_io import write_pickle
from tools.sci import is_a_number

# Paths
dirs = get_configs()
make_output_dirs(dirs)

# Root region definitions
root_regions = RootRegions(conc_dir=dirs.concs)
n_root_regions = root_regions.n_root_regions

# Read dataset
ilo_file = 'Shilling_Matrix_GTAP-AgUnSk'
df = pd.read_excel(dirs.raw + ilo_file + '.xlsx', skiprows=5)