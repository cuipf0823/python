# !/usr/bin/python
# coding=utf-8
from ..proto import cs_basic_pb2 as pb_basic
from . import codec


class StatusCode:
    """
    handle event status code
    """
    SUCCESS = 0
    CONNECT_GM_FAILED = 10000
    SOCK_RECEIVE_ERROR = 10001
    SOCK_SEND_ERROR = 10002
    status_code_desc = {
        0: 'successful',
        10000: 'Connect gm server failed',
        10001: 'Socket receive data failed',
        10002: 'Socket send msg to gm server failed'
    }

    @classmethod
    def status_desc(cls, status_code):
        return cls.status_code_desc.get(status_code, 'status code error, can not find!')

    @classmethod
    def status_and_desc(cls, status_code):
        return status_code, cls.status_code_desc.get(status_code, 'status code error, can not find!')


class Interact:
    """
    manager variables, method that interact with the gm server
    """
    # message sequence number
    msg_seq = 0
    # user session
    session = 0
    # user ID assigned by gm server(maybe not user)
    gid = 0

    def __init__(self):
        pass

    @classmethod
    def seq_num(cls):
        """
        generate message sequence number
        """
        cls.msg_seq += 1
        return cls.msg_seq

    @classmethod
    def make_header(cls, msg_name):
        """
        makeup message header
        """
        header = pb_basic.CSMessageHeader()
        header.msg_name = msg_name.encode('utf-8')
        header.seq_num = cls.seq_num()
        header.gateway_session = cls.session
        return header

    @staticmethod
    def encode(header, body):
        """
        message header and body encode package
        """
        return codec.BaseCodec.encode(header, body)

    @staticmethod
    def decode(data):
        return codec.BaseCodec.decode(data)
