import numpy as np
import pandas as pd
from pathlib import Path

current_working_directory = Path.cwd()

root_country_legend = None

source_root_map = np.random.rand(10, 6357)
root_base_map = pd.read_csv(str(current_working_directory) + '/concs/HSCPC_Eora25_secagg.csv')
source_base_map = np.matmul(source_root_map, np.transpose(root_base_map))