# !/usr/bin/python
# coding=utf-8
from flask import current_app
from flask_login import AnonymousUserMixin
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import redisproxy
from . import login_manager

USER_ROLE = 1
MODERATOR_ROLE = 2
ADMIN_ROLE = 3


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MANAGER_COMMENTS = 0x08
    ADMINISTER = 0x80

    def __init__(self):
        pass


class Role:
    """
    用户角色
    """
    roles = {
        USER_ROLE: (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, True, 'User'),
        MODERATOR_ROLE: (Permission.FOLLOW |
                         Permission.COMMENT |
                         Permission.WRITE_ARTICLES |
                         Permission.MANAGER_COMMENTS, False, 'Moderator'),
        ADMIN_ROLE: (0xff, False, 'Administrator')
        }

    def __init__(self):
        pass

    @staticmethod
    def permissions(role_id):
        if role_id in roles.keys:
            return roles[role_id][0]
        return 0


class AnonymousUser(AnonymousUserMixin):

    @staticmethod
    def can(permissions):
        return False

    @staticmethod
    def is_administrator():
        return False


class User(UserMixin):
    def __init__(self, dicts):
        self._id = dicts['user_id']
        self._username = dicts['name']
        self._password_hash = dicts['password']
        self._email = dicts['email']
        self._role_id = dicts['role_id']
        self._confirmed = dicts['confirmed']

    def verify_password(self, pwd):
        return check_password_hash(self._password_hash, pwd)

    def generate_confirmation_token(self, expiration=3600):
        """
        产生用户确认令牌
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self._id})

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self._id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception as e:
            print e
            return False
        if data.get('confirm') != self._id:
            return False
        self._confirmed = True
        redisproxy.confirm(self._id)
        return True

    def reset_pwd(self, token, new_pwd):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception as e:
            print e
            return False
        if data.get('reset') != self._id:
            return False
        self._password_hash = new_pwd
        return True

    def can(self, permissions):
        return permissions & Role.permissions(self._role_id) == permissions

    def is_administrator(self):
        #return self.can(Permission.ADMINISTER)
        return True

    @property
    def confirmed(self):
        return self._confirmed

    @confirmed.setter
    def confirmed(self, value):
        self._confirmed = value

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
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, value):
        self._password_hash = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def role_id(self):
        return self._role_id

    @role_id.setter
    def role_id(self, value):
        self._role_id = value


def get_user(email):
    user_info = redisproxy.get_user(email)
    if user_info is not None:
        return User(user_info)
    return user_info


def get_user_by_id(user_id):
    user_info = redisproxy.get_user_by_id(user_id)
    if user_info is not None:
        return User(user_info)
    return user_info


def get_user_by_name(name):
    user_info = redisproxy.get_user_by_name(name)
    if user_info is not None:
        return User(user_info)
    return user_info


def register_user(name, pwd, email, role_id):
    return redisproxy.reg_user(name, generate_password_hash(pwd), email, role_id)


def change_password(user_id, pwd):
    return redisproxy.change_password(user_id, generate_password_hash(pwd))


def is_email_register(email):
    return redisproxy.is_email_reg(email)


def is_name_register(username):
    return redisproxy.is_username_reg(username)


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    """
    回调函数，根据用户ID查找用户
    """
    print "user %s login successful" % user_id
    return get_user_by_id(int(user_id))

