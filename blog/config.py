# !/usr/bin/python
# coding=utf-8
import os

# 存储配置
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    GM_LOG_MODE = int(os.environ.get('GM_LOG_MODE'))

    def __init__(self):
        pass

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = False
    GM_SERVER_IP = os.environ.get('GM_SERVER_DEV_IP')
    GM_SERVER_PORT = int(os.environ.get('GM_SERVER_DEV_PORT'))



class TestConfig(Config):
    TESTING = True
    GM_SERVER_IP = os.environ.get('GM_SERVER_TEST_IP')
    GM_SERVER_PORT = int(os.environ.get('GM_SERVER_TEST_PORT'))

config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}

