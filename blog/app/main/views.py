# !/usr/bin/python
# coding=utf-8
from flask import render_template
from flask import redirect, url_for, flash, abort
from flask_login import login_required
from flask_login import current_user
from . import main
from ..models import UserManager


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/user/<user_id>')
def user(user_id):
    user_info = UserManager.get_user_by_id(int(user_id))
    if user_info is None:
        abort(404)
    return render_template('user.html', user=user_info)
