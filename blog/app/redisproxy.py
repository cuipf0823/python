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
    rd.hset('name.to.id', username, user_id)
    return user_id


def get_user(email):
    """
     通过email 获取用户信息
     return dict
    """
    user_id = rd.hget('email.to.id', email)
    if user_id is not None:
        user_info = rd.hmget('user:%s' % user_id, 'name', 'password', 'role_id', 'confirmed')
        user_dict = dict()
        user_dict['user_id'] = int(user_id)
        user_dict['name'] = user_info[0]
        user_dict['password'] = user_info[1]
        user_dict['role_id'] = int(user_info[2])
        user_dict['confirmed'] = (0 if user_info[3] is None else int(user_info[3]))
        user_dict['email'] = email
        return user_dict
    else:
        return None


def get_user_by_name(name):
    """
     通过用户名字获取用户信息
     return dict
    """
    user_id = rd.hget('name.to.id', name)
    if user_id is not None:
        user_info = rd.hmget('user:%s' % user_id, 'email', 'password', 'role_id', 'confirmed')
        user_dict = dict()
        user_dict['user_id'] = int(user_id)
        user_dict['email'] = user_info[0]
        user_dict['password'] = user_info[1]
        user_dict['role_id'] = int(user_info[2])
        user_dict['confirmed'] = (0 if user_info[3] is None else int(user_info[3]))
        user_dict['name'] = name
        return user_dict
    else:
        return None


def get_user_by_id(user_id):
    """
    通过user_id 获取用户信息
    return dict
    """
    user_info = rd.hmget('user:%d' % user_id, 'name', 'password', 'role_id', 'email', 'confirmed')
    if user_info is not None and user_info[0] is not None:
        user_dict = dict()
        user_dict['user_id'] = user_id
        user_dict['name'] = user_info[0]
        user_dict['password'] = user_info[1]
        user_dict['role_id'] = int(user_info[2])
        user_dict['email'] = user_info[3]
        user_dict['confirmed'] = (0 if user_info[4] is None else int(user_info[4]))
        return user_dict
    else:
        return None


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


def is_username_reg(name):
    """
     判断username是否注册过
    """
    return rd.hexists('name.to.id', name)


def confirm(user_id):
    print "redisproxy  confirmed: %d" % user_id
    return rd.hset('user:%d' % user_id, 'confirmed', 1)

