from tornado.web import RequestHandler

from block.block import block_index


class MainHandler(RequestHandler):
    def get(self):
        file_list = block_index.get().keys()
        self.render('index.html', file_list=file_list)
