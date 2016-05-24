import logging

from tornado.web import RequestHandler


class MainHandler(RequestHandler):
    def get(self):
        logging.info('/ is called, redirect now')
        self.redirect('/files')
