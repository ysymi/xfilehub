import os

ROOT = os.path.dirname(__file__)
STORAGE_DIR = os.path.join(ROOT, 'storage')
BLOCKS_FILE = os.path.join(ROOT, 'block', 'block.index')

BUFFER_SIZE = 1024 * 1024

PORT = 5000
