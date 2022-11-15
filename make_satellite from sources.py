from pathlib import Path
from lib.preprocessing import read_reader, concordance_test_runner

print('Making Labour satellite')

current_working_directory = str(Path.cwd())

# Read concordances
source_root_conc = read_reader(current_working_directory + '/concs/ILO_INJ_FATL_ECO_NB_A_EN_22_conc.xlsx')
concordance_test_runner(source_root_conc)

root_base_conc = read_reader(current_working_directory + '/concs/HSCPC_Eora25_secagg.csv')
concordance_test_runner(root_base_conc)

root_country_legend = None



# source_base_map = np.matmul(source_root_map, np.transpose(root_base_map))