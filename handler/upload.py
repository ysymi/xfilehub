from tornado.web import RequestHandler

from config import CHUNK_NAME_FORMAT
from storage.groups import groups
from storage.hashring import hashring


class UploadHandler(RequestHandler):
    def post(self):
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
