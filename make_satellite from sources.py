from pathlib import Path
from lib.preprocessing import concordance_reader, concordance_test_runner
from lib.regions import RootRegions

print('Making Labour satellite')

current_working_directory = str(Path.cwd())

# Read concordances
source_root_conc = concordance_reader(current_working_directory + '/concs/ILO_INJ_FATL_ECO_NB_A_EN_22_conc.xlsx')
concordance_test_runner(source_root_conc)

root_base_conc = concordance_reader(current_working_directory + '/concs/HSCPC_Eora25_secagg.csv')
concordance_test_runner(root_base_conc)

# Root region def
root_regions = RootRegions()



# source_base_map = np.matmul(source_root_map, np.transpose(root_base_map))