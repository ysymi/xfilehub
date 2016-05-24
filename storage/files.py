import json
import logging
import os
import re

from config import FILE_NOTE_PATH
from storage.groups import groups
from util.request import do_request

pat = re.compile(r'(.*).#(\d+)')

class Files(object):
    def __init__(self):
        self._files = {}
        self.recovery()
        if self._files or not self.check():
            self.rebuild()
            self.save()

    def recovery(self):
        if not os.path.exists(FILE_NOTE_PATH):
            logging.info('file.note is not exist')
            return

        with open(FILE_NOTE_PATH, 'r') as f:
            self._files = json.loads(f.read())

    def check(self):
        # TODO check to file map same
        pass

    def rebuild(self):
        for group in groups.get_all():
            chunks_part = do_request('/chunks', group['host'], group['port'], to_dict=True)
            logging.info('chunks_part')
            logging.info(chunks_part)
            chunks = chunks_part['chunks']
            # TODO: parse the chunks into file_map
            for chunk in chunks:
                logging.info(chunk)
                result = pat.match(chunk['name'])
                if result:
                    filename = result.group(1)
                    seq = int(result.group(2))
                    logging.info(filename)
                    logging.info(type(seq))
                    if filename not in self._files:
                        self._files[filename] = {}
                    self._files[filename][seq] = chunk

        self.save()

    def save(self):
        with open(FILE_NOTE_PATH, 'w') as f:
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

        if not self.check():
            self.rebuild()
            self.save()

        return list(self._files.keys())


files = Files()
