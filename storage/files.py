import json
import logging
import os

from config import FILE_MAP_PATH
from storage.groups import group_map
from  util.request import do_request


class Files(object):
    def __init__(self):
        self._file_map = []
        self.recovery()
        if not self._file_map:
            self.rebuild()
            self.save()

    def recovery(self):
        if not os.path.exists(FILE_MAP_PATH):
            logging.info('file.note is not exist')
            return

        with open(FILE_MAP_PATH, 'r') as f:
            self._file_map = json.loads(f.read())

    def rebuild(self):
        groups = group_map.get_all()
        for group in groups:
            chunks_part = do_request('chunks', group.host, group.port)
            # TODO: parse the chunks into file_map

        self.save()

    def save(self):
        with open(FILE_MAP_PATH, 'w') as f:
            f.write(json.dumps(self._file_map, indent=2))

    # TODO: modify
    def insert(self, file_name, md5):
        self._file_map.append({
            'name': file_name,
            'md5': md5,
        })
        self.save()


files = Files()
