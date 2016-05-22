import json
import logging
import os

from config import NODES_NOTE_PATH, STORAGE_PORTS, STORAGE_HOST
from storage.ch import hashring
from util.util import port_is_used


def get_nodes_from_file(path):
    nodes = []
    if not os.path.exists(path):
        logging.info('nodes.note is not exist')
        return nodes

    with open(path, 'r') as f:
        nodes = json.loads(f.read())
    return nodes


def get_nodes_online():
    nodes = []
    for port in STORAGE_PORTS:
        if port_is_used(port):
            node = {
                'name': str(port),
                'host': STORAGE_HOST,
                'port': int(port)

            }
            nodes.append(node)
    return nodes


def get_nodes():
    nodes = get_nodes_from_file(NODES_NOTE_PATH)
    if not nodes:
        nodes = get_nodes_online()
    return nodes


def save_nodes_to_file(nodes):
    with open(NODES_NOTE_PATH, 'w') as f:
        f.write(json.dumps(nodes, indent=2, sort_keys=True))


def nodes_init():
    nodes = get_nodes()

    for node in nodes:
        hashring.add_server(node)
