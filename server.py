import logging

import tornado.ioloop
import tornado.web

from config import LOG_FORMAT
from config import PORT

from handler.file import FileHandler
from handler.chunk import ChunkHandler
from handler.files import FilesHandler
from handler.groups import GroupsHandler
from handler.main import MainHandler
from storage.groups import groups
from storage.hashring import hashring


def make_app():
    settings = {
        'gzip': True,
        'debug': True,
        'static_path': 'static/',
        'template_path': 'template/'
    }
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/files', FilesHandler),
        (r'/groups', GroupsHandler),
        (r'/chunk', ChunkHandler),
        (r'/file/(?P<filename>.*)', FileHandler),
    ], **settings)


def init():
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)

    for group in groups.get_all():
        hashring.insert(group['name'])


if __name__ == '__main__':
    init()
    app = make_app()
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()
