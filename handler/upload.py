import logging
import os

from tornado.web import RequestHandler

from block.block import block_index
from settings import STORAGE_DIR
from util import util


class UploadHandler(RequestHandler):
    def post(self):
        data = self.request.files['data'][0]['body']
        name = self.get_body_argument('name')
        md5 = self.get_body_argument('md5')
        seq = self.get_body_argument('seq')

        logging.info("\nupload:%s\n%s\n%s" % (name + seq, util.md5(data), md5))

        if util.md5(data) == md5:
            block_name = name + '.xb' + seq.zfill(7)
            block_path = os.path.join(STORAGE_DIR, block_name)
            with open(block_path, 'wb') as f:
                f.write(data)
            block_index.update(block_name, md5)
            self.write('ok')
        else:
            self.write_error(400)
