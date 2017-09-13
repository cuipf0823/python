# !/usr/bin/python
# coding=utf-8

import hashlib
import logging
from ..proto import error_code_pb2 as pb_error
from ..proto import gm_pb2
from .common import *


def login_req(tcp_connect, name, pwd, random_bytes):
    req = gm_pb2.GMLoginReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name)
    req.random_bytes = random_bytes
    md5 = hashlib.md5((name + pwd + random_bytes.decode()).encode('utf-8'))
    req.encrypt_bytes = md5.hexdigest().encode('utf-8')
    ret = tcp_connect.send(Interact.encode(header, req))
    return ret


def login_gm(tcp_connect, name, pwd):
    statu_code = 0
    '''
    # fake code
    if statu_code is 0:
        return statu_code, {'name': name, 'pwd': pwd, 'gateway_session': 123456789, 'id': 1}
    '''
    req = gm_pb2.GMCheckSessionReq()
    header = Interact.make_header(req.DESCRIPTOR.full_name)
    header.gateway_session = 0
    req.name = name.encode('utf-8')
    ret_code = tcp_connect.send(Interact.encode(header, req))
    if ret_code != 0:
        logging.error('send msg {} to gm server faild !'.format(req.DESCRIPTOR.full_name))
        return StatusCode.status_and_desc(StatusCode.SOCK_SEND_ERROR)
    ret_code, data = tcp_connect.recv()
    user_info = {'name': name, 'pwd': pwd}
    if ret_code != 0:
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
    ret_code = login_req(tcp_connect, name, pwd, body.random_bytes)
    if ret_code != 0:
        logging.error('send msg CSLoginReq to gm server faild !')
        return StatusCode.status_and_desc(StatusCode.SOCK_SEND_ERROR)
    ret_code, data = tcp_connect.recv()
    if ret_code != 0:
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






