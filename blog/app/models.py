# !/usr/bin/python
# coding=utf-8
from collections import OrderedDict
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from flask_login import AnonymousUserMixin
from . import login_manager
from .dbproxy import DBUserProxy


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
    def __init__(self):
        self._id = 0
        self._username = None
        self._password_hash = None
        self._email = None
        self._role_id = 0
        self._confirmed = False

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
        # 数据库中设置邮箱验证
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
        return self.can(Permission.ADMINISTER)

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


class ManageUser:
    """
    用于管理在线的用户
    """
    def __init__(self):
        self.__users = OrderedDict()
        self.__db = DBUserProxy()

    def get_user(self, email):
        user_info = self.__db.get_user(email)
        print user_info
        if user_info is None:
            return None
        user = User()
        user.id = user_info[0]
        user.username = user_info[1]
        if user.id != 0 and user.username is not None:
            user.password_hash = user_info[2]
            user.role_id = user_info[3]
            user.email = email
            self.__users[user.id] = user
            return user
        return None

    def get_user_by_id(self, user_id):
        if user_id in self.__users.keys():
            return self.__users[user_id]
        return None

    def add_user(self, username, pwd, email):
        # 判断用户角色ID
        if email == current_app.config['MAIL_ADMIN']:
            role_id = ADMIN_ROLE
        else:
            role_id = USER_ROLE
        user_id = self.__db.add_user(username, generate_password_hash(pwd), email, role_id)
        if user_id != 0:
            user = User()
            user.id = user_id
            user.username = username
            user.password_hash = pwd
            user.email = email
            user.role_id = role_id
            self.__users[user_id] = user
            return user
        return None

    def is_email_register(self, email):
        return self.__db.is_register(email)

    def is_user_register(self, username):
        return self.__db.is_user_register(username)

    def change_pwd(self, user_id, pwd):
        """
        用户一定是上线的
        """
        user = self.__users[user_id]
        if user is not None and not user.verify_password(pwd):
            return self.update_pwd(user_id, pwd)
        else:
            return False

    def update_pwd(self, user_id, pwd):
        return self.__db.update_pwd(user_id, generate_password_hash(pwd))

    def reset_pwd(self, user_id, new_pwd):
        return self.update_pwd(user_id, new_pwd)


UsersManager = ManageUser()
login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    """
    回调函数，根据用户ID查找用户
    """
    print "user %s login successful" % user_id
    return UsersManager.get_user_by_id(int(user_id))

