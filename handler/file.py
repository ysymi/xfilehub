import logging

from tornado.web import RequestHandler

from storage.files import files
from util.request import do_request
from util.util import md5


class FileHandler(RequestHandler):
    def get(self, filename):
        logging.info('receive %s ' % filename)
        # return self.redirect('http://127.0.0.1:9000/download/%s' % filename, status=307)

        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + filename)

        chunks = files.get_chunks(filename)  # TODO: get chunks (sort)
        logging.info(chunks)

        for seq, chunk in chunks:
            # chunk = chunks[str(i)]
            logging.info(seq)
            download_url = '/download/%s' % chunk['name']
            data = do_request(download_url, chunk['host'], chunk['port'], is_file=True)
            if data is None:
                logging.error('Data  is  None   !!!!')
            logging.info('down from %s' % download_url)

            logging.info('md5: %s ' % md5(data))

            self.write(data)

            # TODO error process
            pass

        self.finish()
