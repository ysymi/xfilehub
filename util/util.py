import hashlib


def md5(data):
    if isinstance(data, (str, bytes)):
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()
    else:
        return ''
