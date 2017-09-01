#!/usr/bin/python
# -*- coding: utf-8 -*-
import struct
from google.protobuf import reflection
from ..proto import cs_basic_pb2 as basic_pb
from ..proto import gm_pb2 as gm_pb

# 协议头部表示长度字节数
MSG_LEN_BYTES = 8
HEADER_LEN_BYTES = 4


class BaseCodec(object):
    """
    提供pb协议的编解码方案
    """
    @staticmethod
    def decode(data):
        """
        协议解包
        :param data: 二进制字符串
        :return:header，body
        """
        if len(data) > MSG_LEN_BYTES:
            header = basic_pb.CSMessageHeader()
            msg_len, header_len = struct.unpack('=II', data[:MSG_LEN_BYTES])
            fmt = '%ds%ds' % (header_len - HEADER_LEN_BYTES, msg_len - MSG_LEN_BYTES - (header_len - HEADER_LEN_BYTES))
            str_header, str_body = struct.unpack(fmt, data[MSG_LEN_BYTES:])
            header.ParseFromString(str_header)
            msg_name = header.msg_name.decode()
            if msg_name == 'ErrorCode':
                body = reflection.ParseMessage(basic_pb.DESCRIPTOR.message_types_by_name[msg_name], str_body)
                return header, body
            body = reflection.ParseMessage(gm_pb.DESCRIPTOR.message_types_by_name[msg_name.split('.')[-1]], str_body)
            return header, body
        else:
            print('data len: %d less than proto min len' % MSG_LEN_BYTES)
        return

    @staticmethod
    def encode(header, body):
        """
        协议打包
        :param header:消息头
        :param body: 消息体
        :return:打包完成的消息二进制字符串
        """
        header_len = header.ByteSize() + HEADER_LEN_BYTES
        msg_len = MSG_LEN_BYTES + header.ByteSize() + body.ByteSize()
        fmt = '=II%ds%ds' % (header.ByteSize(), body.ByteSize())
        return struct.pack(fmt, msg_len, header_len, header.SerializeToString(), body.SerializeToString())

