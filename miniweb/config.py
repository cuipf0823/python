# !/usr/bin/python
# coding=utf-8
import os
# 存储配置
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'guess string'
    MAIL_SERVER = 'smtp.163.com'  # 电子邮件服务器的主机名或IP地址
    MAIL_PORT = '25'  # 电子邮件服务器的端口
    MAIL_USE_TLS = True  # 启用传输层安全
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # 邮件账户用户名
    MAIL_PASSWORD = os.environ.get('MAIL_PWD')  # 邮件账户的密码
    MAIL_SUBJECT_PREFIX = '[Miniweb]'

    def __init__(self):
        pass

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DB_IP = os.environ.get('DB_DEV_IP')
    DB_USERNAME= os.environ.get('DB_DEV_USERNAME')
    DB_PWD = os.environ.get('DB_DEV_PWD')
    DB_NAME = os.environ.get('DB_DEV_NAME')



class TestConfig(Config):
    TESTING = True
    DB_IP = os.environ.get('DB_DEV_IP')
    DB_USERNAME= os.environ.get('DB_DEV_USERNAME')
    DB_PWD = os.environ.get('DB_DEV_PWD')
    DB_NAME = os.environ.get('DB_DEV_NAME')


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}

