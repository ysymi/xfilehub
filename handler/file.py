from tornado.web import RequestHandler

from config import CHUNK_NAME_FORMAT
from storage.groups import groups
from storage.hashring import hashring


class FileHandler(RequestHandler):
    def post(self, *args, **kwargs):
        name = self.get_body_argument('name')
        seq = self.get_body_argument('seq')
        chunk_name = CHUNK_NAME_FORMAT % (name, seq)

        group_name = hashring.find(chunk_name)
        group = groups.get(group_name)

        upload_url = 'http://%{host}s:%{port}/upload' % (group.host, group.prot)

        return self.redirect(upload_url, status=307)

        #
        #
        #
        #
        #
        # # self.set_header()
        #
        # md5 = self.get_body_argument('md5')
        # data = self.request.files['data'][0]['body']
        #
        #
        # logging.info("\nupload:%s\n%s\n%s" % (name + seq, util.md5(data), md5))
        #
        # if util.md5(data) == md5:
        #     block_name = name + '.xb' + seq.zfill(7)
        #     block_path = os.path.join(STORAGE_DIR, block_name)
        #     with open(block_path, 'wb') as f:
        #         f.write(data)
        #     block_index.update(block_name, md5)
        #     self.write('ok')
        # else:
        #     self.write_error(400)

    def get(self, *args, **kwargs):

            filename = self.get_argument('filename')
            return self.redirect('http://127.0.0.1:9000/download/%s' % filename, status=307)

            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition', 'attachment; filename=' + filename)

            blocks = sorted(block_index.get()[filename])
            for block, md5 in blocks:
                block_path = os.path.join(STORAGE_DIR, block)
                with open(block_path, 'rb') as f:
                    data = f.read()
                    logging.info("\ndownload:%s\n%s\n%s" % (filename, util.md5(data), md5))

                    if util.md5(data) == md5:
                        self.write(data)
                    else:
                        # TODO error process
                        pass

            self.finish()
            pass

