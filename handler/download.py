import logging
import os

from tornado.web import RequestHandler

from block.block import block_index
from config import STORAGE_DIR
from util import util


class DownloadHandler(RequestHandler):
    def get(self):

        filename = self.get_argument('filename')
        return self.redirect('http://127.0.0.1:9000/download/%s' % filename, status=307)

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
