# !/usr/bin/python
# coding=utf-8

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_login import LoginManager
from config import config
from flask_wtf import CSRFProtect
import sys
import logging

bootstrap = Bootstrap()
moment = Moment()
login_manager = LoginManager()
csrf = CSRFProtect()
# 防止会话被篡改，设置为strong，会记录客户端的IP和浏览器的用户代理信息
login_manager.session_protection = 'strong'
# 设置登录页面的端点
login_manager.login_view = 'auth.login'
gm_server_ip = None
gm_server_port = 0


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 初始化
    bootstrap.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    if config[config_name].GM_LOG_MODE == 1:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
                            format='%(asctime)s %(levelname)-8s %(message)s --%(filename)s:%(lineno)-4d')
    else:
        logging.basicConfig(level=logging.DEBUG, filename='gm_tool.log',
                            format='%(asctime)s %(levelname)-8s %(message)s --%(filename)s:%(lineno)-4d')

    global gm_server_ip
    gm_server_ip = config[config_name].GM_SERVER_IP
    global gm_server_port
    gm_server_port = config[config_name].GM_SERVER_PORT

    # 注册蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    # url_prefix为可选参数，如果设置，注册后的蓝本中定义的所有路由都会加上指定的前缀
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    return app
