import logging

from tornado.web import RequestHandler

from storage.files import files
from util.request import do_request


class FileHandler(RequestHandler):
    def get(self, filename):
        logging.info('recive %s ' % filename)
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
