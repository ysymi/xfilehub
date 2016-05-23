import logging

import tornado.ioloop
import tornado.web

from config import PORT
from handler.download import DownloadHandler
from handler.main import MainHandler
from handler.upload import UploadHandler
from storage.groups import get_groups
from storage.hashring import hashring

from config import LOG_FORMAT


def make_app():
    settings = {
        'gzip': True,
        'debug': True,
        'static_path': 'static/',
        'template_path': 'template/'
    }
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/upload', UploadHandler),
        (r'/download', DownloadHandler),
    ], **settings)


def init():
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)

    groups = get_groups()
    for group in groups:
        hashring.insert(group.name)


if __name__ == '__main__':
    init()
    app = make_app()
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
