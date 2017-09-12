#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import select
import struct
import time
import logging


MAX_RECEIVE_BUF = 64 * 1024  # 64k


class TcpConnection(object):
    """
    tcp连接、接收和发送
    """
    STATUS_SUCCESS = 0
    STATUS_ERR = -1

    def __init__(self, ip, port):
        self.__ip = ip
        self.__port = port
        self.__sock = None

    def __del__(self):
        self.close()

    @property
    def sock_id(self):
        return self.__sock.fileno()

    @property
    def is_connect(self):
        if self.__sock is not None and self.__sock.fileno() >= 0:
            return True
        return False

    def connect(self):
        address = (self.__ip, self.__port)
        if self.__sock is not None:
            logging.info('Connect gm server already sock id:{}'.format(self.sock_id))
            return False
        count = 0
        while count < 3:
            try:
                self.__sock = socket.socket()
                self.__sock.connect(address)
            except socket.error as err:
                self.close()
                time.sleep(1)
                count += 1
                logging.error('Connect ip:{0}:port:{1} failed {2}...Try reconnect {3} time.'.format(
                    self.__ip, self.__port, err, count))
                continue
            break
        if self.__sock is None or count >= 3:
            return False
        self.__sock.settimeout(4.0)
        logging.info('Connect GM Server successfully!')
        return True

    def select(self, time_out):
        """
        select mode
        """
        return select.select([self.__sock], [], [], time_out)

    def send(self, data):
        data_len = len(data)
        ret = 0
        while True:
            try:
                ret = self.__sock.send(data[ret:])
            except socket.error as err:
                logging.error('socket send data faild error:'.format(err))
                return self.STATUS_ERR
            if ret >= data_len:
                break
        return self.STATUS_SUCCESS

    def recv(self):
        """
        接收数据 保证接收的是完整包
        :return status_code, 返回完整包数据
        """
        all_data = ''.encode('utf-8')
        while True:
            try:
                rec_data = self.__sock.recv(MAX_RECEIVE_BUF)
            except socket.error as err:
                logging.error('socket recv error: '.format(err))
                return self.STATUS_ERR, err
            if len(rec_data) > 0:
                all_data += rec_data
                if len(all_data) > 4:
                    msg_len = struct.unpack('=I', all_data[:4])
                else:
                    continue
                if len(all_data) >= msg_len[0]:
                    break
        return self.STATUS_SUCCESS, all_data

    def close(self):
        if self.__sock is not None:
            self.__sock.close()
            self.__sock = None
