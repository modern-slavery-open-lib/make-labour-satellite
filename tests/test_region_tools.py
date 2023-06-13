from lib.configs import get_configs
from lib.regions import RootRegions

# Directories
dirs, _ = get_configs()

# Region definitions
root_regions = RootRegions(conc_dir=dirs.concs)


def test_region_match_aus():
    assert root_regions.find_region_id_from_name('Australia') == 12


def test_region_match_iran():
    assert root_regions.find_region_id_from_name('Iran') == 92


def test_region_match_bvi():
    assert root_regions.find_region_id_from_name('British Virgin Islands') == 212

