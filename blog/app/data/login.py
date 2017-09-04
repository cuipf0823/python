# !/usr/bin/python
# coding=utf-8

import hashlib
import logging
from ..proto import error_code_pb2 as pb_error
from ..proto import gm_pb2
from .. import tcp_connect
from .common import *


def login_req(name, pwd, random_bytes):
    req = gm_pb2.GMLoginReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name)
    req.random_bytes = random_bytes
    md5 = hashlib.md5((name + pwd + random_bytes.decode()).encode('utf-8'))
    req.encrypt_bytes = md5.hexdigest().encode('utf-8')
    tcp_connect.send(Interact.encode(header, req))


def login_gm(name, pwd):
    statu_code = 0
    '''
    # fake code
    if statu_code is 0:
        return statu_code, {'name': name, 'pwd': pwd, 'gateway_session': 123456789, 'id': 1}
    '''
    # 连接gm 服务器
    if not tcp_connect.connect():
        return StatusCode.status_and_desc(StatusCode.CONNECT_GM_FAILED)
    req = gm_pb2.GMCheckSessionReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name)
    header.gateway_session = 0
    req.name = name.encode('utf-8')
    tcp_connect.send(Interact.encode(header, req))
    data = tcp_connect.recv()
    user_info = {'name': name, 'pwd': pwd}
    if not data:
        logging.error('receive gm server response message faild !')
        return StatusCode.status_and_desc(StatusCode.SOCK_RECEIVE_ERROR)
    header, body = Interact.decode(data)
    if header.errcode != 0:
        logging.error('user {0} send {1} to gm server error {2}!'.format(name, req.DESCRIPTOR.full_name,
                                                                         header.errcode))
        return header.errcode, pb_error.GMErrorCode.Name(header.errcode)
    Interact.session = header.gateway_session
    user_info.setdefault('gateway_session', header.gateway_session)
    logging.debug('user {0} check session successfully random bytes {1}'.format(name, body.random_bytes))
    login_req(name, pwd, body.random_bytes)
    data = tcp_connect.recv()
    if not data:
        logging.error('receive gm server response message faild !')
        return StatusCode.status_and_desc(StatusCode.SOCK_RECEIVE_ERROR)
    header, rsp = Interact.decode(data)
    if header.errcode != 0:
        logging.error('user {0} send CSLoginReq to gm server error {1}!'.format(name, header.errcode))
        return header.errcode, pb_error.GMErrorCode.Name(header.errcode)
    if rsp.HasField('gid'):
        Interact.gid = rsp.gid
        user_info.setdefault('id', Interact.gid)
    else:
        Interact.gid += 1
        user_info.setdefault('id', Interact.gid)
    logging.info('user {0} login gm server sucessfully gid: {1}'.format(name, Interact.  gid))
    return statu_code, user_info






