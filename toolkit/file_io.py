import json
import os
import pickle


def write_pickle(fname, obj_to_write):

    with open(fname, 'wb') as f:
        pickle.dump(obj_to_write, f)


def read_pickle(fname):

    with open(fname, 'rb') as pickle_file:
        result = pickle.load(pickle_file)

    return result


def read_json_from_disk(fname):

    assert os.path.isfile(fname), fname + ' does not exist.'

    with open(fname) as json_file:
        data = json.load(json_file)

    return data