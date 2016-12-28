# !/usr/bin/python
# coding=utf-8

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from config import config
import MySQLdb
import os


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = None
login_manager = LoginManager()
# 防止会话被篡改，设置为strong，会记录客户端的IP和浏览器的用户代理信息
login_manager.session_protection = 'strong'
# 设置登录页面的端点
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 初始化
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    global db
    db = MySQLdb.connect(config[config_name].DB_IP, config[config_name].DB_USERNAME,
                         config[config_name].DB_PWD, config[config_name].DB_NAME)
    login_manager.init_app(app)

    # 注册蓝图
    from main import blue
    from auth import auth as auth_blueprint
    app.register_blueprint(blue)
    # url_prefix为可选参数，如果设置，注册后的蓝本中定义的所有路由都会加上指定的前缀
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    return app