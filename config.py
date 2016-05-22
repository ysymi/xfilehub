import os

ROOT = os.path.dirname(__file__)
STORAGE_DIR = os.path.join(ROOT, 'storage')
BLOCKS_FILE = os.path.join(ROOT, 'block', 'block.index')

PORT = 5000
BUFFER_SIZE = 1024 * 1024

CHUNK_NOTE_PATH = os.path.join(STORAGE_DIR, 'chunk.note')
NODES_NOTE_PATH = os.path.join(STORAGE_DIR, 'nodes.note')

STORAGE_PORTS = list(range(8000, 8010))
STORAGE_HOST = 'localhost'
