import os
import logging
import shutil
from tornado.web import RequestHandler

from block.block import block_index
from settings import STORAGE_DIR,BUFFER_SIZE


class DownloadHandler(RequestHandler):
    def get(self):
        filename = self.get_argument('filename')
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + filename)

        blocks = sorted(block_index.get()[filename])
        tmp = open(os.path.join(STORAGE_DIR, filename), "wb")

        for block in blocks:
            logging.info(block)
            block_path = os.path.join(STORAGE_DIR, block)
            with open(block_path, "rb") as f:
                data = f.read()
                self.write(data)
                tmp.write(data)

        tmp.close()

        # 记得有finish哦
        self.finish()
        pass
