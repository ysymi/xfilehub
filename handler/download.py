import logging
import os

from tornado.web import RequestHandler

from block.block import block_index
from settings import STORAGE_DIR


class DownloadHandler(RequestHandler):
    def get(self):
        filename = self.get_argument('filename')
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + filename)

        blocks = sorted(block_index.get()[filename])

        for block in blocks:
            block_path = os.path.join(STORAGE_DIR, block)
            with open(block_path, "rb") as f:
                self.write(f.read())

        self.finish()
        pass
