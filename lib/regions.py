import pandas as pd
from toolkit.sets import is_empty
from toolkit.sci import is_a_number


class RootRegions:

    def __init__(self, conc_dir=None):
        region_legend = pd.read_excel(conc_dir + '/RootRegionLegend.xlsx', header=0)
        self.region_legend = region_legend
        self.n_root_regions = region_legend.shape[0]

    def find_region_id_from_name(self, country):
        """
            Matches a given country name string in the alias columns of the region legend
        """

        assert isinstance(country, str)

        region_legend = self.region_legend
        cols = region_legend.columns.to_list()
        col_idx = cols.index('OfficialName')

        # Check each alias column for a match
        match_idx = None
        i = col_idx
        while match_idx is None and i < len(cols):
            col_name = cols[i]
            subset = region_legend.loc[(region_legend[col_name] != 'ZZZZ') & (region_legend[col_name] == country)]
            if not is_empty(subset):
                assert subset.shape[0] == 1, 'More than one match discovered!'
                match_idx = subset['Root country number'].values[0]
            i = i + 1

        # Check if match was found
        if match_idx is None:
            return None
        else:
            # Tests
            assert is_a_number(match_idx) and 1 <= match_idx <= self.n_root_regions

            return match_idx
