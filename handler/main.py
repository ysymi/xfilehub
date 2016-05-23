from tornado.web import RequestHandler


class MainHandler(RequestHandler):
    def get(self):
        self.redirect('/files')
