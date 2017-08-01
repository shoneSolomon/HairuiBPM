import hashlib


def md5(val):
    m = hashlib.md5()
    m.update(str(val).encode('utf-8'))
    return m.hexdigest()