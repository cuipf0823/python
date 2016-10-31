# !/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import make_response
from flask import render_template
from flask_bootstrap import Bootstrap

app=Flask(__name__)
bootstrap = Bootstrap(app)


# index 试图函数
@app.route('/')
def index():
    return "<h1>Hello World!</h1>"


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
    return render_template('404.html'), 404


# 有未处理的异常的时候
@app.errorhandler(500)
def internal_server_error(e):
    return 'Sorry, 500server error!'


if __name__ == '__main__':
    app.run(debug=True)