from pathlib import Path
import os
import re
import json

current_working_directory = Path.cwd()


class Bunch:

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    root = None
    object = None
    raw = None
    concs = None
    processed = None
    satellite = None
    mrio_format = None


def get_configs():

    root_directory = re.match("(.*make-labour-satellite)", str(current_working_directory)).group(1) + "/"

    # Directories
    object_dir = root_directory + 'objects/'
    dirs = Bunch(root=root_directory,
                 object=object_dir,
                 raw=object_dir + 'raw/',
                 concs=object_dir + 'concs/',
                 processed=object_dir + 'processed/',
                 satellite=object_dir + 'satellite/',
                 )

    # Settings
    config_fname = root_directory + '/' + 'config.json'
    with open(config_fname) as json_file:
        config_file = json.load(json_file)

    config = Bunch(sec_root_to_base_conc=config_file["sector_root_to_base_conc"],
                   reg_root_to_base_conc=config_file["region_root_to_base_conc"],
                   mrio_format=config_file["mrio_format"],
                   satellite_settings=config_file["satellite_settings"]
                   )

    assert config.mrio_format in ['SUT', 'IIOT']

    return dirs, config


def make_output_dirs(dirs):
    """
        Creates save directories, if not already created
    """

    if not os.path.isdir(dirs.processed):
        os.mkdir(dirs.processed)

    if not os.path.isdir(dirs.satellite):
        os.mkdir(dirs.satellite)

