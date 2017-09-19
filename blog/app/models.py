# !/usr/bin/python
# coding=utf-8
from datetime import datetime
from flask import request
from flask_login import UserMixin
from .data import login, query
from . import login_manager
from . import gm_server_ip, gm_server_port
from .tcp_con import TcpConnection
import hashlib
import logging
import time


class User(UserMixin):
    def __init__(self, dicts):
        self.__id = dicts.get('id', 1)
        self.__username = dicts.get('name')
        self.__password = dicts.get('pwd')
        self.__gateway_session = dicts.get('gateway_session')
        self.__login_time = datetime.strptime(str(datetime.utcnow()), '%Y-%m-%d %H:%M:%S.%f')
        self.__connect_gm = None

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        vhash = hashlib.md5(self.username.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=vhash, size=size, default=default, rating=rating)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def password(self):
        return self.__password

    @property
    def gateway_session(self):
        return self.__gateway_session

    @gateway_session.setter
    def gateway_session(self, value):
        self.__gateway_session = value

    @property
    def login_time(self):
        return self.__login_time

    @property
    def connect_gm(self):
        return self.__connect_gm

    @connect_gm.setter
    def connect_gm(self, value):
        self.__connect_gm = value

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return '(user_id: {0.__id}, user_name: {0.__username}, gateway_session: {0.__gateway_session})'.format(self)


class UserManager:
    """
    storage current user already logining
    """
    users = {}

    def __init__(self):
        pass

    @classmethod
    def get_user_by_id(cls, user_id):
        return cls.users.get(user_id)

    @classmethod
    def append(cls, user):
        return cls.users.setdefault(user.id, user)

    @classmethod
    def remove(cls, user_id):
        del cls.users[user_id]

    @classmethod
    def print_users(cls):
        for key, value in cls.users.items():
            logging.debug(value)

    @classmethod
    def get_user_by_name(cls, name):
        for _, value in cls.users.items():
            if value.username == name:
                return value
        return None


class OnlineServers:
    servers = []
    # 最后更新时间
    last_time = 0

    def __init__(self):
        pass

    @classmethod
    def update(cls, servers):
        cls.servers = servers
        cls.last_time = time.time()


def is_already_login(name, pwd):
    user = UserManager.get_user_by_name(name)
    if user is not None and user.password == pwd and user.connect_gm.is_connect:
        return True
    return False


def login_gm(name, pwd):
    """
     login success return statu_code = 0 and User
     login faild return statu_code = error_code and error describe
    """
    tcp_connect = TcpConnection(gm_server_ip, gm_server_port)
    if not tcp_connect.connect():
        return 10000, 'Connect gm server failed'
    status_code, ret = login.login_gm(tcp_connect, name, pwd)
    logging.info('user:{0} pwd: {1} login status_code: {2}, user_info: {3}'.format(name, pwd, status_code, ret))
    if status_code == 0:
        user = User(ret)
        user.connect_gm = tcp_connect
        return status_code, user
    return status_code, ret


def query_operators():
    return query.Operations.operations()


def query_callback(opt, user, **kwargs):
    return query.Operations.callback(opt, user, **kwargs)


def query_response_cb(opt, rsp):
    if opt == query.Operations.OPT_LIST_SERVER:
        OnlineServers.update(query.handle_list_server(rsp))
    elif opt == query.Operations.OPT_ONLINES_SERVER:
        OnlineServers.update(query.handle_online_server(rsp))


def callback_type():
    return query.CallBackType


@login_manager.user_loader
def load_user(user_id):
    """
    回调函数，根据用户ID查找用户
    """
    logging.debug('user {} login successful'.format(user_id))
    return UserManager.get_user_by_id(int(user_id))









