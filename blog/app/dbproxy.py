# !/usr/bin/python
# coding=utf-8

from werkzeug.security import generate_password_hash
from . import db


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

    def __init__(self):
        self.__con = db
        self.__table_name = 'blog_users'

    # 先不考虑db的关闭
    def __del__(self):
        pass

    # 获取玩家
    def get_user(self, email):
        cursor = self.__con.cursor()
        sqlstr = "SELECT id, user_name, pwd_hash, role_id FROM %s WHERE email = '%s' " % (self.__table_name, email)
        cursor.execute(sqlstr)
        ret = cursor.fetchone()
        cursor.close()
        return ret

    # 邮件地址是否注册过
    def is_register(self, email):
        cur = self.__con.cursor()
        sqlstr = "SELECT * FROM %s WHERE email = '%s' " % (self.__table_name, email)
        cur.execute(sqlstr)
        ret = cur.fetchall()
        cur.close()
        return len(ret)

    # 用户名字是否注册过
    def is_user_register(self, username):
        cur = self.__con.cursor()
        sqlstr = "SELECT * FROM %s WHERE user_name = '%s' " % (self.__table_name, username)
        cur.execute(sqlstr)
        ret = cur.fetchall()
        cur.close()
        return len(ret)

    def add_user(self, username, pwd, email):
        cur = self.__con.cursor()
        sqlstr = "INSERT into %s (user_name, pwd_hash, email, role_id, reg_time) VALUES " \
                 "('%s', '%s', '%s', %u, NOW())" % (self.__table_name, username, generate_password_hash(pwd), email, 0)
        cur.execute(sqlstr)
        self.__con.commit()
        cur.close()

