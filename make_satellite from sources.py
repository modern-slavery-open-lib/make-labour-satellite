import numpy as np
from pathlib import Path
from lib.preprocessing import read_aggregator

current_working_directory = str(Path.cwd())

root_country_legend = None

source_root_map = np.random.rand(10, 6357)
root_base_map = read_aggregator(current_working_directory + '/concs/HSCPC_Eora25_secagg.csv')
source_base_map = np.matmul(source_root_map, np.transpose(root_base_map))