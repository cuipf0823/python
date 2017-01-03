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
from . import auth
from ..models import User, add_user
from .forms import LoginForm
from .forms import RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User()
        ret = user.get_user(form.email.data)
        if ret and user.verify_password(form.password.data):
            login_user(user, form.rem_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password!')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out!')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('You can login now.')
        add_user(form.username.data, form.password.data, form.email.data)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)




