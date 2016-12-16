# !/usr/bin/python
# coding=utf-8

from flask import Blueprint
# import views
# import errors


# 实例化Blueprint类对象创建蓝本
blue = Blueprint('blue', __name__)

from . import views
from . import errors


