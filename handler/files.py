from tornado.web import RequestHandler

from storage.files import files
import logging


class FilesHandler(RequestHandler):
    def get(self):
        logging.info('/files called')
        file_list = files.get_files()
        self.render('index.html', file_list=file_list)
