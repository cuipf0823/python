# !/usr/bin/python
# coding=utf-8

from . import rd


def reg_user(username, pwd, email, role_id):
    """
    添加新用户  传递hash 之后的pwd 返回用户ID值
    """
    user_id = rd.incr('users:count')
    # 保存用户信息
    rd.hmset('user:%d' % user_id, {'name': username, 'password': pwd, 'email': email, 'role_id': role_id})
    rd.hset('email.to.id', email, user_id)
    return user_id


def get_user(email):
    """
     通过email 获取用户信息
     return dict
    """
    user_id = rd.hget(email)
    if user_id != 0:
        user_info = rd.hmget('user:%d' % user_id, 'name', 'password', 'role_id', 'confirmed')
        user_dict['user_id'] = user_id
        user_dict['name'] = user_info[0]
        user_dict['password'] = user_info[1]
        user_dict['role_id'] = user_info[2]
        user_dict['confirmed'] = user_info[3]
        user_dict['email'] = email
        return user_dict
    else:
        return None


def get_user_by_id(user_id):
    """
    通过user_id 获取用户信息
    return list（）
    """
    user_info = rd.hmget('user:%d' % user_id, 'name', 'password', 'role_id', 'email', 'confirmed')
    if user_info is not None:
        user_dict['user_id'] = user_id
        user_dict['name'] = user_info[0]
        user_dict['password'] = user_info[1]
        user_dict['role_id'] = user_info[2]
        user_dict['email'] = user_info[3]
        user_dict['confirmed'] = user_info[4]
        return user_dict
    else:
        return user_info


def change_password(user_id, pwd):
    """
    修改用户密码
    """
    return rd.hset('user:%d' % user_id, 'password', pwd)


def is_email_reg(email):
    """
    判断email是否注册过
    """
    return rd.hexists('email.to.id', email)


def is_user_reg(name):
    pass

