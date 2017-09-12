# !/usr/bin/python
# coding=utf-8
from flask import render_template, url_for, flash
from flask import request, redirect
from flask_login import login_user, logout_user
from . import auth
from ..models import login_gm, User, UserManager
from .forms import LoginForm
from .. import tcp_connect


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        status_code, ret = login_gm(form.username.data, form.password.data)
        if status_code is 0:
            UserManager.append(User(ret))
            login_user(User(ret))
            # ret = init_server()
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('login gm server failed {0}:{1}'.format(status_code, ret), 'error')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    # 关闭tcp连接
    tcp_connect.close()
    flash('You have been logged out!')
    return redirect(url_for('auth.login'))


# 程序可以决定用户确认账户之前可以做什么操作，允许未确认账户登录，但是只显示一个页面，要求用户在获取权限之前先确认账户
# 使用before_request 钩子完成 before_request钩子只能应用于属于蓝本的请求上；
# 全局钩子，必须使用before_app_request修饰器

@auth.before_app_request
def before_request():
    return







