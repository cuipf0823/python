# !/usr/bin/python
# coding=utf-8


def to_str(bytes_or_str):
    """
    python3 接受str或者bytes字符串, 返回str
    """
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value


def to_bytes(bytes_or_str):
    """
    python3 接受str或者bytes字符串, 返回bytes
    """
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value


def to_unicode(unicode_to_str):
    """
    python2 接受str或unicode 返回unicode
    """
    if isinstance(unicode_to_str, str):
        value = unicode_to_str.decode('utf-8')
    else:
        value = unicode_to_str
    return value


def to_str_py2(unicode_to_str):
    """
    python2 接受str或unicode 返回unicode
    """
    if isinstance(unicode_to_str, unicode):
        value = unicode_to_str.encode('utf-8')
    else:
        value = unicode_to_str
    return value


def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        found = int(found[0])
    else:
        found = default
    return found
