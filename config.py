import os
import socket

PORT = 9000
BUFFER_SIZE = 1024 * 1024

ROOT = os.path.dirname(__file__)
STORAGE_DIR = os.path.join(ROOT, 'storage')
FILE_NOTE_PATH = os.path.join(STORAGE_DIR, 'files.note')
GROUPS_NOTE_PATH = os.path.join(STORAGE_DIR, 'groups.note')

GET_IP_CMD = 'ifconfig| grep 192.168 | awk \'{print $2}\''
STORAGE_HOST = os.popen(GET_IP_CMD).read().strip()  # TODO: ready for no network environment
STORAGE_PORTS = list(range(8000, 8010))

LOGGING_FORMAT = '%(asctime)s %(levelname)s %(message)s'
CHUNK_NAME_FORMAT = '{filename}.chunk{seq:0>3}'
