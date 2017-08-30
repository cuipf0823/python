#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import select
import struct
import time
import logging
from .. import tcp_sock


MAX_RECEIVE_BUF = 64 * 1024  # 64k


def send(data):
    data_len = len(data)
    ret = 0
    while True:
        ret = tcp_sock.send(data[ret:])
        if ret >= data_len:
            break
    return


def recv():
    """
    接收数据 保证接收的是完整包
    :return 返回完整包数据
    """
    all_data = ''.encode('utf-8')
    while True:
        rec_data = tcp_sock.recv(MAX_RECEIVE_BUF)
        if len(rec_data) > 0:
            all_data += rec_data
            if len(all_data) > 4:
                msg_len = struct.unpack('=I', all_data[:4])
            else:
                continue
            if len(all_data) >= msg_len[0]:
                break
        else:
            # 服务端主动关闭
            break
    return all_data


def close():
    tcp_sock.close()
