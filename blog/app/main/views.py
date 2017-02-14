# !/usr/bin/python
# coding=utf-8
from flask import render_template
from . import main
from ..models import get_user_by_name


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user_info = get_user_by_name(username)
    if user_info is None:
        abort(404)
    print type(user_info.last_seen)
    print user_info.last_seen
    return render_template('user.html', user=user_info)
