import os

from tornado.web import RequestHandler

from block.block import block_index
from settings import STORAGE_DIR


class UploadHandler(RequestHandler):
    def post(self):
        data = self.request.files['data'][0]['body']
        name = self.get_body_argument("name")
        seq = self.get_body_argument("seq")

        block_name = name + ".xb" + seq.zfill(7)
        block_path = os.path.join(STORAGE_DIR, block_name)
        with open(block_path, "wb") as f:
            f.write(data)

        block_index.update(block_name)
        self.write("ok")
