# !/usr/bin/python
# coding=utf-8

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
import MySQLdb
import os
from config import config


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = None


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    print(app.config['MAIL_SERVER'])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    global db
    db = MySQLdb.connect(config[config_name].DB_IP, config[config_name].DB_USERNAME,
                         config[config_name].DB_PWD, config[config_name].DB_NAME)
    # 注册蓝图
    from main import blue
    app.register_blueprint(blue)
    return app