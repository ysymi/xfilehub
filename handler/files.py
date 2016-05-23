from tornado.web import RequestHandler

from storage.files import files


class FilesHandler(RequestHandler):
    def get(self):
        file_list = files.get_files()
        self.render('index.html', file_list=file_list)
