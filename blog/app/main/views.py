# !/usr/bin/python
# coding=utf-8
from flask import render_template
from flask import redirect, url_for, abort
from flask_login import current_user
from . import main
from ..models import UserManager
from ..data import operations
import logging


@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', operations=operations.Operations.operations())
    return redirect(url_for('auth.login'))


@main.route('/user/<user_id>')
def user(user_id):
    user_info = UserManager.get_user_by_id(int(user_id))
    if user_info is None:
        abort(404)
    return render_template('user.html', user=user_info)


@main.route('/query/<opt>')
def query(opt):
    logging.debug('query {} from gm server'.format(opt))
    ret = operations.Operations.callback(opt)
    print(type(ret.response))
    print(ret.response)
    print(str(ret.response))
    return render_template('index.html', operations=operations.Operations.operations(), response=str(ret.response))
