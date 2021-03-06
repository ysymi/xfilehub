import logging
import time

import tornado.ioloop
import tornado.web

from config import LOGGING_FORMAT
from config import PORT
from handler.chunks import ChunksHandler
from handler.file import FileHandler
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
        'template_path': 'template/'  # todo: Bug : fix bug cwd not xfilehub
    }
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/chunks', ChunksHandler),
        (r'/files', FilesHandler),
        (r'/files/(?P<filename>.*)', FileHandler),
        (r'/groups', GroupsHandler),
    ], **settings)


def init():
    logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)

    while hashring.size() != 10:
        logging.info('try to insert groups to hashring')
        for group_name, group_info in groups.get_all().items():
            hashring.insert(group_name)
            logging.info('insert %s to hashring' % group_name)
        time.sleep(0.5)

    logging.info('haring has %s group' % hashring.size())


if __name__ == '__main__':
    app = make_app()
    app.listen(PORT)
    init()
    logging.info('front server running at %s' % PORT)
    tornado.ioloop.IOLoop.current().start()
