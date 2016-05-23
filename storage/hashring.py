import hashlib


class HashRing(object):
    def __init__(self, groups=None, replica=3):
        self._replica = replica
        self._virtual_groups = []
        self._group = {}
        if groups:
            for group in groups:
                self.insert(group)

    def insert(self, group):
        for i in range(self._replica):
            virtual_group = "%s#%s" % (group, i)
            key = self._gen_key(virtual_group)
            self._group[key] = group
            self._virtual_groups.append(key)
        self._virtual_groups.sort()

    def remove(self, group):
        for i in range(self._replica):
            virtual_group = "%s#%s" % (group, i)
            key = self._gen_key(virtual_group)
            del self._group[key]
            self._virtual_groups.remove(key)

    def find(self, data):
        if self._virtual_groups:
            key = self._gen_key(data)
            for group_key in self._virtual_groups:
                if key <= group_key:
                    return self._group[group_key]
            return self._group[self._virtual_groups[0]]
        else:
            return None

    @staticmethod
    def _gen_key(data):
        result = hashlib.md5(data).hexdigest()
        return int(result, 16)


hashring = HashRing()
