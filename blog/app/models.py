# !/usr/bin/python
# coding=utf-8

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from . import db
from . import login_manager


# 数据库中检测名字是否存在
def check_name(name):
    cursor = db.cursor()
    sqlstr = "SELECT * FROM %s WHERE NICK = '%s'" % ('t_ru_base', name)
    # print(sqlstr)
    cursor.execute(sqlstr)
    ret = cursor.fetchall()
    db.commit()
    cursor.close()
    return ret


class User(UserMixin):
    def __init__(self, pwd):
        self._pwd_hash = generate_password_hash(pwd)
        pass

    @property
    def password(self):
        return self._pwd_hash

    @password.setter
    def password(self, pwd):
        self._pwd_hash = generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self._pwd_hash, pwd)


# 回调函数，根据用户ID查找用户
@login_manager.user_loader
def load_user(user_id):
    # return User.query.get(int(user_id))
    return None

