import pandas as pd
import re
from pathlib import Path

current_working_directory = str(Path.cwd())
root_directory = re.match("(.*make-labour-satellite)", current_working_directory).group(1)
region_legend = pd.read_excel(root_directory + '/concs/RootRegionLegend.xlsx', header=0)


class RootRegions:

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    n_root_regions = region_legend.shape[0]