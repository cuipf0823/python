# !/usr/bin/python
# coding=utf-8
from datetime import datetime
from flask import request
from flask_login import UserMixin
from .data import login
from . import login_manager
import hashlib
import logging

# maximum number of articles per page
POST_NUM_PAGE = 10


class User(UserMixin):
    def __init__(self, dicts):
        self.__id = dicts.get('id', 1)
        self.__username = dicts.get('name')
        self.__password = dicts.get('pwd')
        self.__gateway_session = dicts.get('gateway_session')
        self.__login_time = datetime.strptime(str(datetime.utcnow()), '%Y-%m-%d %H:%M:%S.%f')

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
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def gateway_session(self):
        return self.__gateway_session

    @gateway_session.setter
    def gateway_session(self, value):
        self.__gateway_session = value

    @property
    def login_time(self):
        return self.__login_time

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
        return '(user_id: {0.__id}, user_name: {0.__username}, gateway_session: {0.__gateway_session})'.format(self)


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


class Pagination:
    def __init__(self, page, items, total, per_page=POST_NUM_PAGE):
        # the current page number
        self._page = page
        # the number of items to be displayed on a page
        self._per_page = per_page
        # the total number
        self._total = total
        # the items for the current page
        self._items = items
        # the total number of pages
        if self._per_page == 0:
            self._pages = 0
        else:
            self._pages = int(math.ceil(self._total / float(self._per_page)))

    @property
    def page(self):
        return self._page

    @property
    def pages(self):
        return self._pages

    @property
    def total(self):
        return self._total

    @property
    def items(self):
        return self._items

    @property
    def pre_page(self):
        return self._per_page

    @property
    def has_prev(self):
        """
         return True if a previous page exists
        """
        return self._page > 1

    @property
    def has_next(self):
        """
         return True if a next page exists
        """
        return self._pages > self._page

    @property
    def pre_num(self):
        """
         number of the previous page.
        """
        if self.has_prev:
            return self._page - 1

    @property
    def next_num(self):
        """
         number of the next page
        """
        if self.has_next:
            return self._page + 1

    def next(self):
        """
        return a class Ragination
        """
        assert self.has_next, 'must be has next'
        return Pagination(self.next_num, posts_by_page(self.next_num), self.total)

    def prev(self):
        """
        return a class Ragination
        """
        assert self.has_prev, 'must be has prev'
        return Pagination(self.pre_num, posts_by_page(self.pre_num), self.total)

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
                    (self._page - left_current - 1 < num < self._page + right_current) or \
                    (num > self._pages - right_edge):
                if last + 1 != num:
                    yield None
                yield num
                last = num


def login_gm(name, pwd):
    """
     login success return statu_code = 0 and User
     login faild return statu_code = error_code and error describe
    """
    return login.login_gm(name, pwd)


@login_manager.user_loader
def load_user(user_id):
    """
    回调函数，根据用户ID查找用户
    """
    logging.debug('user {} login successful'.format(user_id))
    return UserManager.get_user_by_id(int(user_id))
