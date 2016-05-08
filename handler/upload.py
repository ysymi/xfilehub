import os

from tornado.web import RequestHandler

from block import block_index
from settings import STORAGE_PATH


class UploadHandler(RequestHandler):
    def post(self):
        data = self.request.files['data'][0]['body']
        name = self.get_body_argument("name")
        seq = self.get_body_argument("seq")

        blockname = name + seq.zfill(10)
        block_index.update(blockname)
        file_path = os.path.join(STORAGE_PATH, blockname)
        with open(file_path, "wb") as f:
            f.write(data)

        self.write("ok")
