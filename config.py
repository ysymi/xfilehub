import os

ROOT = os.path.dirname(__file__)
STORAGE_DIR = os.path.join(ROOT, 'storage')
BLOCKS_FILE = os.path.join(ROOT, 'block', 'block.index')

PORT = 9000
BUFFER_SIZE = 1024 * 1024

LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'

CHUNK_NOTE_PATH = os.path.join(STORAGE_DIR, 'chunk.note')
GROUPS_NOTE_PATH = os.path.join(STORAGE_DIR, 'groups.note')

STORAGE_PORTS = list(range(8000, 8010))
STORAGE_HOST = 'localhost'


FILE_MAP_PATH = os.path.join(STORAGE_DIR, 'files')
CHUNK_NAME_FORMAT = '%{name}s.#%{seq}s'
