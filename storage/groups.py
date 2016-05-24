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
        if not self._groups or not self.check():
            self.rebuild()
            self.save()

    def recovery(self):
        if not os.path.exists(GROUPS_NOTE_PATH):
            logging.info('group.note is not exist')
            return
        with open(GROUPS_NOTE_PATH, 'r') as f:
            self._groups = json.loads(f.read())

    def check(self):  # TODO reduce replica
        online_groups = []
        for port in STORAGE_PORTS:
            if port_is_used(port):
                info = do_request('/info', STORAGE_HOST, port, to_dict=True)
                 # logging.info(info)
                group = {
                    'name': info['name'],
                    'host': info['host'],
                    'port': info['port'],
                    # 'master': info.masters,
                    # 'slaves': info.slaves
                }
                online_groups.append(group)
        logging.info('online groups : %s  self.grups: %s' % (len(online_groups), len(self._groups)))
        return len(self._groups) == len(online_groups)

    def rebuild(self):
        self._groups = []
        for port in STORAGE_PORTS:
            if port_is_used(port):
                info = do_request('/info', STORAGE_HOST, port, to_dict=True)  # TODO finish /info
                # logging.info(info)
                group = {
                    'name': info['name'],
                    'host': info['host'],
                    'port': info['port'],
                    # 'master': info.masters,
                    # 'slaves': info.slaves
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

    def get(self, name):
        for group in self._groups:
            if group['name'] == name:
                return group
        return None

    def get_all(self):
        if not self.check():
            self.rebuild()
            self.save()
        return self._groups


groups = Groups()
