import json
import os
import logging

from settings import BLOCK_FILE, STORAGE_PATH


class BlockIndex(object):
    def __init__(self):
        self._block_index = {}

    def get(self):
        if os.path.exists(BLOCK_FILE):
            with open(BLOCK_FILE, 'r') as f:
                self._block_index = json.loads(f.read())
            return self._block_index

        block_list = os.listdir(STORAGE_PATH)
        logging.info(block_list)
        for block_name in block_list:
            self.update(block_name)
        return self._block_index

    def update(self, block_name):
        filename = block_name[:-10]
        if filename not in self._block_index:
            self._block_index[filename] = []
        self._block_index[filename].append(block_name)
        self.save()

    def save(self):
        with open(BLOCK_FILE, 'w') as f:
            f.write(json.dumps(self._block_index))


block_index = BlockIndex()
