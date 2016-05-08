import os

from tornado.web import RequestHandler

from settings import STORAGE_PATH


class UploadHandler(RequestHandler):
    def post(self):
        data = self.request.files['data'][0]['body']
        name = self.get_body_argument("name")
        seq = self.get_body_argument("seq")

        filename = name + seq.zfill(10)
        file_path = os.path.join(STORAGE_PATH, filename)
        with open(file_path, "wb") as f:
            f.write(data)

        self.write("ok")
