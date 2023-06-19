from toolkit.dict import match_key_in_dlist
from toolkit.file_io import read_json_from_disk
from toolkit.sets import is_empty


class Indexer:

    def __init__(self, object_dir=None):
        self.file_index = read_json_from_disk(object_dir + '/index.json')

    def infill_option(self, dataset_id=None):

        assert dataset_id is not None

        index_rec = match_key_in_dlist(self.file_index, 'dataset_id', dataset_id)
        assert not is_empty(index_rec)

        if 'fill_missing_from_totals' in index_rec[0] and index_rec[0]['fill_missing_from_totals'] is True:
            infill_missing = True
        else:
            infill_missing = False

        return infill_missing
