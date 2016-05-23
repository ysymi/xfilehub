import json
import logging
import os

from config import GROUPS_NOTE_PATH, STORAGE_PORTS, STORAGE_HOST
from util.request import do_request
from util.util import port_is_used


class Groups(object):
    def __init__(self):
        self._groups = []
        self.recovery()
        if not self._groups:
            self.rebuild()
            self.save()

    def recovery(self):
        if not os.path.exists(GROUPS_NOTE_PATH):
            logging.info('group.note is not exist')
            return
        with open(GROUPS_NOTE_PATH, 'r') as f:
            self._groups = json.loads(f.read())

    def rebuild(self):
        for port in STORAGE_PORTS:
            if port_is_used(port):
                info = do_request('info', STORAGE_HOST, port)  # TODO finish /info
                group = {
                    'name': str(port),
                    'host': STORAGE_HOST,
                    'master': info.masters,
                    'slaves': info.slaves
                }
                self._groups.append(group)
        self.save()

    def save(self):
        with open(GROUPS_NOTE_PATH, 'w') as f:
            f.write(json.dumps(self._groups, indent=2))

    # TODO: check this is used
    def insert(self, group_name, md5):
        self._groups.append({
            'name': group_name,
            'md5': md5,
        })
        self.save()


groups = Groups()
