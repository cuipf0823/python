# !/usr/bin/python
# coding=utf-8

from . import db


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