# !/usr/bin/python
# coding=utf-8

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from . import login_manager
from .dbproxy import DBUserProxy
db = DBUserProxy()


# 判断email是否注册过
def is_register(email):
    return db.is_register(email)


# 判断用户名是否注册过
def is_user_register(username):
    return db.is_user_register(username)


# 添加用户
def add_user(username, pwd, email):
    return db.add_user(username, pwd, email)


class User(UserMixin):
    def __init__(self):
        self.id = 0
        self._user_name = None
        self._pwd_hash = None
        self._email = None
        self._role_id = 0
        self._db_user = db

    def get_user(self, email):
        user_info = self._db_user.get_user(email)
        self.id = user_info[0]
        self._user_name = user_info[1]
        if self.id != 0 and self._user_name is not None:
            self._pwd_hash = user_info[2]
            self._role_id = user_info[3]
            self._email = email
            return True
        return False

    @property
    def password(self):
        return self._pwd_hash

    @password.setter
    def password(self, pwd):
        # 暂时不添加修改数据库操作
        self._pwd_hash = generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self._pwd_hash, pwd)


# 回调函数，根据用户ID查找用户
@login_manager.user_loader
def load_user(user_id):
    # return User.query.get(int(user_id))
    print "user %s login successful" % user_id
    return None

