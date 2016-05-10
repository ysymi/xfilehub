import logging
import os

from tornado.web import RequestHandler

from block.block import block_index
from settings import STORAGE_DIR
from util import util


class DownloadHandler(RequestHandler):
    def get(self):
        filename = self.get_argument('filename')
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + filename)

        blocks = sorted(block_index.get()[filename])
        for block, md5 in blocks:
            block_path = os.path.join(STORAGE_DIR, block)
            with open(block_path, 'rb') as f:
                data = f.read()
                logging.info("\ndownload:%s\n%s\n%s" % (filename, util.md5(data), md5))

                if util.md5(data) == md5:
                    self.write(data)
                else:
                    # todo error process
                    pass

        self.finish()
        pass
