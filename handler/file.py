from tornado.web import RequestHandler

from config import CHUNK_NAME_FORMAT
from storage.files import files
from storage.groups import groups
from storage.hashring import hashring
from util.request import do_request


class FileHandler(RequestHandler):
    def post(self):
        name = self.get_body_argument('name')
        seq = self.get_body_argument('seq')
        chunk_name = CHUNK_NAME_FORMAT % (name, seq)

        group_name = hashring.find(chunk_name)
        group = groups.get(group_name)

        upload_url = 'http://%{host}s:%{port}/upload' % (group.host, group.port)

        return self.redirect(upload_url, status=307)

    def get(self, filename):
        # return self.redirect('http://127.0.0.1:9000/download/%s' % filename, status=307)

        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + filename)

        chunks = files.get_chunks(filename)  # TODO: get chunks (sort)
        for chunk in chunks:
            download_url = '/download/%s' % chunk.name
            data = do_request(download_url, chunk.host, chunk.port)

            self.write(data)

            # TODO error process
            pass

        self.finish()
