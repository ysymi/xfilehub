import json
import logging
import os

from config import CHUNK_NOTE_PATH
from storage.groups import get_nodes
from util.request import do_request


def get_chunks_from_file(path):
    chunks = []
    if not os.path.exists(path):
        logging.info('chunk.note is not exist')
        return chunks

    with open(path, 'r') as f:
        chunks = json.loads(f.read())
    return chunks


def get_chunks_online():
    chunks = []
    nodes = get_nodes()
    for node in nodes:
        chunks_part = do_request('chunks', node.host, node.port)
        chunks += chunks_part
    return chunks


def get_chunks():
    chunks = get_chunks_from_file(CHUNK_NOTE_PATH)
    if not chunks:
        chunks = get_chunks_online()
    return chunks


def save_chunks_to_file(chunks):
    with open(CHUNK_NOTE_PATH, 'w') as f:
        f.write(json.dumps(chunks, indent=2, sort_keys=True))
