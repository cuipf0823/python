# !/usr/bin/python
# coding=utf-8

from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import flash
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user
from . import auth
from ..models import login_gm, User, UserManager
from .forms import LoginForm
from .forms import RegistrationForm
from .forms import ChangePwdForm
from .forms import PasswordResetForm
from .forms import PasswordResetRequestForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        status_code, ret = login_gm(form.username.data, form.password.data)
        if status_code is 0:
            UserManager.append(User(ret))
            UserManager.print()
            login_user(User(ret), form.rem_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('login gm server failed {0}:{1}'.format(status_code, ret), 'error')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('main.index'))


# 程序可以决定用户确认账户之前可以做什么操作，允许未确认账户登录，但是只显示一个页面，要求用户在获取权限之前先确认账户
# 使用before_request 钩子完成 before_request钩子只能应用于属于蓝本的请求上；
# 全局钩子，必须使用before_app_request修饰器

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))







