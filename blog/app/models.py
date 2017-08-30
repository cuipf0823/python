# !/usr/bin/python
# coding=utf-8
from datetime import datetime
from flask import current_app, request
from flask_login import UserMixin
from .data import db_users
from . import login_manager
import hashlib
import logging


class User(UserMixin):
    def __init__(self, dicts):
        self._id = dicts.get('id', 1)
        self._username = dicts.get('name')
        self._password = dicts.get('pwd')
        self._gateway_session = dicts.get('gateway_session')

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
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def gateway_session(self):
        return self._gateway_session

    @gateway_session.setter
    def gateway_session(self, value):
        self._gateway_session = value

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
        return '(user_id: {0._id}, user_name: {0._username}, gateway_session: {0._gateway_session})'.format(self)


class UserManager:
    """
    storage current user already logining
    """
    users = {}

    @classmethod
    def get_user_by_id(cls, user_id):
        return cls.users.get(user_id)

    @classmethod
    def append(cls, user):
        return cls.users.setdefault(user.id, user)

    @classmethod
    def print(cls):
        for key, value in cls.users.items():
            logging.debug(value)


def login_gm(name, pwd):
    """
     login success return statu_code = 0 and User
     login faild return statu_code = error_code and error describe
    """
    return db_users.login_gm(name, pwd)


@login_manager.user_loader
def load_user(user_id):
    """
    回调函数，根据用户ID查找用户
    """
    logging.debug('user {} login successful'.format(user_id))
    return UserManager.get_user_by_id(int(user_id))
