import json
import logging
import os

from config import FILE_MAP_PATH
from storage.groups import groups
from util.request import do_request


class Files(object):
    def __init__(self):
        self._files = {}
        self.recovery()
        if not self._files:
            self.rebuild()
            self.save()

    def recovery(self):
        if not os.path.exists(FILE_MAP_PATH):
            logging.info('file.note is not exist')
            return

        with open(FILE_MAP_PATH, 'r') as f:
            self._files = json.loads(f.read())

    def rebuild(self):
        for group in groups.get_all():
            chunks_part = do_request('/chunks', group['host'], group['port'])
            logging.info('chunks_part')
            logging.info(chunks_part)
            # TODO: parse the chunks into file_map

        self.save()

    def save(self):
        with open(FILE_MAP_PATH, 'w') as f:
            f.write(json.dumps(self._files, indent=2))

    # # TODO: modify
    # def insert(self, file_name, md5):
    #     self._files.append({
    #         'name': file_name,
    #         'md5': md5,
    #     })
    #     self.save()

    def get_chunks(self, filename):
        if filename in self._files:
            return self._files[filename]
        return None

    def get_files(self):

        return list(self._files.keys())


files = Files()
