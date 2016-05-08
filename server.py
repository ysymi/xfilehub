import logging

import tornado.ioloop
import tornado.web

from handler.download import DownloadHander
from handler.main import MainHandler
from handler.upload import UploadHandler


def make_app():
    settings = {
        'debug': True,
        'static_path': 'static/',
        'template_path': 'template/'
    }
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/download', DownloadHander),
        (r'/upload', UploadHandler)
    ], **settings)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
