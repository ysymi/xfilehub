import os

from tornado.web import RequestHandler

from block import block_index
from settings import STORAGE_PATH


class DownloadHander(RequestHandler):
    def get(self):
        filename = self.get_argument('filename')
        buf_size = 1024 * 1024
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + filename)

        blocks = block_index.get()[filename]
        for block in blocks:
            block_path = os.path.join(STORAGE_PATH, block)

            with open(block_path, "rb") as f:
                while True:
                    data = f.read(buf_size)
                    if not data:
                        break
                    self.write(data)

        # 记得有finish哦
        self.finish()
        pass
