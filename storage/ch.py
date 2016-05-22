import hashlib


class HashRing(object):
    def __init__(self, servers=None, replica=3):
        self._replica = replica
        self._virtual_servers = []
        self._server = {}
        if servers:
            for server in servers:
                self.add_server(server)

    def add_server(self, server):
        for i in range(self._replica):
            virtual_server = "%s#%s" % (server, i)
            key = self._gen_key(virtual_server)
            self._server[key] = server
            self._virtual_servers.append(key)
        self._virtual_servers.sort()

    def remove_server(self, server):
        for i in range(self._replica):
            virtual_server = "%s#%s" % (server, i)
            key = self._gen_key(virtual_server)
            del self._server[key]
            self._virtual_servers.remove(key)

    def get_server(self, key_str):
        if self._virtual_servers:
            key = self._gen_key(key_str)
            for server_key in self._virtual_servers:
                if key <= server_key:
                    return self._server[server_key]
            return self._server[self._virtual_servers[0]]
        else:
            return None

    @staticmethod
    def _gen_key(key_str):
        result = hashlib.md5(key_str).hexdigest()
        return int(result, 16)


hashring = HashRing()
