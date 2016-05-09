import json
import logging
import os

from settings import BLOCKS_FILE, STORAGE_DIR


class BlockIndex(object):
    def __init__(self):
        self._block_index = {}
        if os.path.exists(BLOCKS_FILE):
            with open(BLOCKS_FILE, 'r') as f:
                self._block_index = json.loads(f.read())
        else:
            self.sync()

    def get(self):
        if len(self._block_index) > 0 and self.test():
            return self._block_index

        self.sync()
        return self._block_index

    def test(self):
        logging.info(self._block_index)
        for file, blocks in self._block_index.items():
            logging.info("%s %s" % (file, blocks))
            for block in blocks:
                logging.info(block)
                block_path = os.path.join(STORAGE_DIR, block)
                if not os.path.exists(block_path):
                    return False
        return True

    def update(self, block_name):
        filename = block_name[:-10]
        if filename not in self._block_index:
            self._block_index[filename] = []
        self._block_index[filename].append(block_name)
        self.save()  # maybe cost too much or try to solve blocks in disk but no index in mem

    def sync(self):
        self._block_index = {}
        block_list = os.listdir(STORAGE_DIR)
        for block_name in block_list:
            self.update(block_name)
        self.save()
        return self._block_index

    def save(self):
        with open(BLOCKS_FILE, 'w') as f:
            f.write(json.dumps(self._block_index, indent=2, sort_keys=True))


block_index = BlockIndex()
