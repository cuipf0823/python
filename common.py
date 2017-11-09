# !/usr/bin/python
# coding=utf-8


def convert(data):
    """
    编码方式转换为utf-8, 支持字典,元组直接传入
    """
    if isinstance(data, bytes):
        return data.decode('utf-8')
    if isinstance(data, dict):
        return dict(map(convert, data.items()))
    if isinstance(data, tuple):
        return map(convert, data)
    return data
