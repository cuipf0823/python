# !/usr/bin/python
# coding=utf-8

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from . import db
from . import login_manager

'''
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
'''


class DBUserProxy:
    def __init__(self, connect):
        self.__con = connect
        self.__table_name = 'blog_users'

    # 获取玩家
    def get_user(self, email):
        cursor = self.__con.cursor()
        sqlstr = "SELECT id, user_name, pwd_hash, role_id FROM %s WHERE email = '%s' " % (self.__table_name, email)
        cursor.execute(sqlstr)
        return cursor.fetchone()


class User(UserMixin):
    def __init__(self):
        self.id = 0
        self._user_name = None
        self._pwd_hash = None
        self._email = None
        self._role_id = 0
        self._db_user = DBUserProxy(db)

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

