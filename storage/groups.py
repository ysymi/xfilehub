import json
import logging
import os

from config import GROUPS_NOTE_PATH, STORAGE_PORTS, STORAGE_HOST
from util.request import do_request
from util.util import port_is_used


class Groups(object):
    def __init__(self):
        self._groups = {}
        self.recovery()
        if not self._groups or not self.check():
            self.rebuild()

    def recovery(self):
        if not os.path.exists(GROUPS_NOTE_PATH):
            logging.info('group.note is not exist')
            return

        with open(GROUPS_NOTE_PATH, 'r') as f:
            self._groups = json.loads(f.read())

    def check(self):  # TODO reduce replica
        if len(self._groups) == len(STORAGE_PORTS):
            return True

        logging.info('check groups now')
        # online_groups = self.collect()
        # logging.info('online groups : %s  self.grups: %s' % (len(online_groups), len(self._groups)))
        return len(self._groups) == len(self.collect())

    def rebuild(self):
        self._groups = self.collect()
        self.save()

    def save(self):
        with open(GROUPS_NOTE_PATH, 'w') as f:
            f.write(json.dumps(self._groups, indent=2, sort_keys=True))

    @staticmethod
    def collect():
        online_groups = {}
        for port in STORAGE_PORTS:
            if port_is_used(port):
                try:
                    info = do_request('/info', STORAGE_HOST, port, to_dict=True)  # TODO finish /info
                    group = {
                        'host': info['host'],
                        'port': info['port']
                    }
                    online_groups[info['name']] = group
                except Exception as e:
                    logging.exception('can not get info of %s, %s' % (port, str(e)))

        return online_groups

    # TODO: check this is used
    # def insert(self, group_name, md5):
    #     self._groups.append({
    #         'name': group_name,
    #         'md5': md5,
    #     })
    #     self.save()

    def get(self, name):
        if name in self._groups.keys():
            return self._groups[name]
        return None

    def get_all(self):
        logging.info('get all groups')
        if len(self._groups) == 0 or not self.check():
            logging.info('will rebuild groups')
            self.rebuild()
        return self._groups


groups = Groups()
