from pathlib import Path
import os
import re

current_working_directory = Path.cwd()


class Bunch:

    def __init__(self, **kwds):
        self.__dict__.update(kwds)

    object = None
    concs = None
    processed = None
    satellite = None


def get_configs():

    # Directories
    root_directory = re.match("(.*make-labour-satellite)", str(current_working_directory)).group(1) + "/"
    object_dir = root_directory + 'objects/'
    dirs = Bunch(root=root_directory,
                 object=object_dir,
                 raw=object_dir + 'raw/',
                 concs=object_dir + 'concs/',
                 processed=object_dir + 'processed/',
                 satellite=object_dir + 'satellite/',
                 )

    return dirs


def make_output_dirs(dirs):
    if not os.path.isdir(dirs.processed):
        os.mkdir(dirs.processed)

    if not os.path.isdir(dirs.satellite):
        os.mkdir(dirs.satellite)

