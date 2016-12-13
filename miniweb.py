# !/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_script import Manager
from flask import session
from flask import redirect
from flask import url_for
from flask import flash
# from flask_mysqldb import MySQL
import MySQLdb
import datetime

app=Flask(__name__)
# app.config 字典可以用来存储框架、扩展和程序本身的配置变量
# SECRET_KEY 配置变量是通用密钥
app.config['SECRET_KEY'] = 'gress string'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

dbcon = MySQLdb.connect('10.1.1.119', 'ru', '123456', 'ru_30007')
'''
# index 试图函数
@app.route('/')
def index():
    return "<h1>Hello World!</h1>"
'''


# 接受动态参数
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello %s!</h1>' % name


# 获取上下文
@app.route('/context')
def context():
    agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s </p>' % agent


@app.route('/rsp')
def response():
    rsp_str = make_response('<h1> this docment carries a cookies !</h1>')
    rsp_str.set_cookie('answer', 42)
    return rsp_str


# 使用模板，渲染模板
@app.route('/login/<name>')
def login(name):
    return render_template('login.html', name=name)


# 使用flask-bootstrap
@app.route('/check/<name>')
def cheak(name):
    return render_template('check.html', name=name)


# 错误页面处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', current_time=datetime.datetime.utcnow()), 404


# 有未处理的异常的时候
@app.errorhandler(500)
def internal_server_error(e):
    return 'Sorry, 500server error!'


# 表单类提交
class NameForm(FlaskForm):
    # 文本字段
    name = StringField('What is your name:', validators=[DataRequired()])
    # 名字为Entry的提交按钮
    submit = SubmitField('Entry')


# web 表单
@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)


# web 表单重定向
@app.route('/re', methods=['GET', 'POST'])
def index_re():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index_re'))
    return render_template('index.html', form=form, name=session.get('name'))


# flash 消息
@app.route('/flash', methods=['GET', 'POST'])
def index_flash():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('looks like you changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index_flash'))
    return render_template('index.html', form=form, name=session.get('name'))


# 数据库中检测名字是否存在
def check_name(name):
    cursor = dbcon.cursor()
    sqlstr = "SELECT * FROM %s WHERE NICK = '%s'" % ('t_ru_base', name)
    print(sqlstr)
    cursor.execute(sqlstr)
    ret = cursor.fetchall()
    dbcon.commit()
    cursor.close()
    return ret


# 检测输入用户是否在数据库中
@app.route('/sql', methods=['GET', 'POST'])
def index_sql():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('looks like you changed your name!')
        session['name'] = form.name.data
        if len(check_name(form.name.data)) == 0:
            session['exist'] = False
            flash('you name not in sql')
        else:
            session['exist'] = True
        return redirect(url_for('index_sql'))
    return render_template('index.html', form=form, name=session.get('name'), exist=session.get('exist'))


if __name__ == '__main__':
    app.run(debug=True)