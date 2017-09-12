# !/usr/bin/python
# coding=utf-8
from datetime import datetime
from flask import request
from flask_login import UserMixin
from .data import login
from . import login_manager
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
    def gateway_session(self):
        return self.__gateway_session

    @gateway_session.setter
    def gateway_session(self, value):
        self.__gateway_session = value

    @property
    def login_time(self):
        return self.__login_time

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
    def print_users(cls):
        for key, value in cls.users.items():
            logging.debug(value)


def login_gm(name, pwd):
    """
     login success return statu_code = 0 and User
     login faild return statu_code = error_code and error describe
    """
    return login.login_gm(name, pwd)


@login_manager.user_loader
def load_user(user_id):
    """
    回调函数，根据用户ID查找用户
    """
    logging.debug('user {} login successful'.format(user_id))
    return UserManager.get_user_by_id(int(user_id))


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






