import logging

from tornado.web import RequestHandler

from config import CHUNK_NAME_FORMAT
from storage.groups import groups
from storage.hashring import hashring


class ChunksHandler(RequestHandler):
    def post(self):
        name = self.get_body_argument('name')
        seq = self.get_body_argument('seq')
        chunk_name = CHUNK_NAME_FORMAT.format(filename=name, seq=seq)

        logging.info('get chunk: %s' % chunk_name)
        group_name = hashring.find(chunk_name)
        group = groups.get(group_name)

        logging.info('will save to %s' % group_name)

        upload_url = 'http://{host}:{port}/upload'.format(host=group['host'], port=group['port'])
        logging.info(upload_url)
        return self.redirect(upload_url, status=307)
