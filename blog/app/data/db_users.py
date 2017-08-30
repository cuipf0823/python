# !/usr/bin/python
# coding=utf-8

from . import tcp_con
from . import proto_codec
from ..proto import cs_basic_pb2 as pb_basic
from ..proto import gm_pb2
from ..proto import error_code_pb2 as pb_error
import hashlib
import logging

msg_seq = 0
gateway_session = 0
gid = 0

ERRCODE = {
        0: 'mail config parse successful',
        10000: 'socket receive data failed',
        10001: 'mail title is empty or beyond max len 64',
        10002: 'mail content is empty or beyond max len 1024',
        10003: 'mail sender is empty or beyond max len 32',
        10004: 'mail vaild time config error',
        10005: 'mail is destory flag config error',
        10006: 'mail priority flag config error',
        10007: 'mail is popping flag config error',
        10008: 'mail receiver info config error',
        10009: 'mail delayed time config error'
    }


def encode(header, body):
    return proto_codec.BaseCodec.encode(header, body)


def seq_num():
    global msg_seq
    msg_seq += 1
    return msg_seq


def make_header(msg_name):
    header = pb_basic.CSMessageHeader()
    header.msg_name = msg_name.encode('utf-8')
    header.seq_num = seq_num()
    header.gateway_session = gateway_session
    return header


def login_req(name, pwd, random_bytes):
    req = gm_pb2.GMLoginReq()
    header = make_header(req.DESCRIPTOR.full_name)
    req.random_bytes = random_bytes
    md5 = hashlib.md5((name + pwd + random_bytes.decode()).encode('utf-8'))
    req.encrypt_bytes = md5.hexdigest().encode('utf-8')
    tcp_con.send(encode(header, req))


def login_gm(name, pwd):
    req = gm_pb2.GMCheckSessionReq()
    header = make_header(req.DESCRIPTOR.full_name)
    header.gateway_session = 0
    req.name = name.encode('utf-8')
    tcp_con.send(encode(header, req))
    data = tcp_con.recv()
    user_info = {'name': name, 'pwd': pwd}
    statu_code = 0
    if not data:
        statu_code = 1000
        logging.error('receive gm server response message faild !')
        return statu_code, ERRCODE.get(statu_code)
    header, body = proto_codec.BaseCodec.decode(data)
    if header.errcode != 0:
        logging.error('user {0} send {1} to gm server error {2}!'.format(name, req.DESCRIPTOR.full_name,
                                                                         header.errcode))
        return header.errcode, pb_error.GMErrorCode.Name(header.errcode)
    global gateway_session
    gateway_session = header.gateway_session
    user_info.setdefault('gateway_session', header.gateway_session)
    logging.debug('user {0} check session successfully random bytes {1}'.format(name, body.random_bytes))
    login_req(name, pwd, body.random_bytes)
    data = tcp_con.recv()
    if not data:
        statu_code = 1000
        logging.error('receive gm server response message faild !')
        return statu_code, ERRCODE.get(statu_code)
    header, rsp = proto_codec.BaseCodec.decode(data)
    if header.errcode != 0:
        logging.error('user {0} send CSLoginReq to gm server error {1}!'.format(name, header.errcode))
        return header.errcode, pb_error.GMErrorCode.Name(header.errcode)
    if rsp.HasField('gid'):
        global gid
        gid = rsp.gid
        user_info.setdefault('id', gid)
    else:
        gid += 1
        user_info.setdefault('id', gid)
    logging.info('user {0} login gm server sucessfully gid: {1}'.format(name, gid))
    return statu_code, user_info






