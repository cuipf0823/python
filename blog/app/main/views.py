# !/usr/bin/python
# coding=utf-8
from flask import render_template
from flask import redirect, url_for, abort
from flask_login import current_user
from . import main
from ..models import UserManager
from ..data import operations
from .forms import PlayerForm, ServerForm, MailForm
import logging
import datetime
import time

DEFAULT_MAIL_SENDER = '纸盒人星球官方'


def init_time(days=15):
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=days)
    valid_time = now + delta
    return valid_time

def calc_second(str_time):
    return  time.mktime(time.strptime(str_time, '%Y-%m-%d %H:%M:%S')) - time.time()


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


def handle_query_mail(form):
    mail_info = {}
    mail_info.setdefault('title', form.title.data)
    mail_info.setdefault('sender', form.sender.data)
    mail_info.setdefault('content', form.content.data)
    mail_info.setdefault('valid_time', calc_second(form.valid_time.data))
    mail_info.setdefault('delayed_time', calc_second(form.delayed_time.data))
    mail_info.setdefault('is_popping', form.is_popping.data)
    mail_info.setdefault('priority', form.priority.data)
    mail_info.setdefault('is_destory', form.is_destory.data)


@main.route('/query/<int:param_type>/<opt>', methods=['GET', 'POST'])
def query(param_type, opt):
    logging.debug('query {0} from gm server type: {1}'.format(opt, param_type))
    if param_type == operations.CallBackType.PARAM_NONE:
        ret = operations.Operations.callback(opt)
        # 更新内存数据
        operations.Operations.rsp_callback(opt, ret.response)
        return render_template('index.html', operations=operations.Operations.operations(), response=str(ret.response))
    elif param_type == operations.CallBackType.PARAM_UID_CHANNEL:
        form = PlayerForm()
        if form.validate_on_submit():
            uid = form.uid.data
            channel = form.channel.data
            logging.debug('query {0} from gm server uid: {1}, channel: {2}'.format(opt, uid, channel))
            ret = operations.Operations.callback(opt, uid=uid, channel=channel)
            return render_template('index.html', operations=operations.Operations.operations(),
                                   form=form, response=str(ret.response))
        form.channel.data = 0
        return render_template('index.html', operations=operations.Operations.operations(), form=form)
    elif param_type == operations.CallBackType.PARAM_SERVER_ID:
        form = ServerForm()
        if form.validate_on_submit():
            server_id = int(form.server_id.data)
            ret = operations.Operations.callback(opt, server_id=server_id)
            return render_template('index.html', operations=operations.Operations.operations(),
                                   form=form, response=str(ret.response))
        return render_template('index.html', operations=operations.Operations.operations(), form=form)
    elif param_type == operations.CallBackType.PARAM_MAIL:
        form = MailForm()
        if form.validate_on_submit():
            logging.debug('title:{0}, sender:{1}, valid_time:{2}, delayed_time:{3}'.format(
                form.title.data, form.sender.data, form.valid_time.data, form.delayed_time.data))
            print(form.mail_receiver.data)
            return render_template('index.html', operations=operations.Operations.operations(),
                                   form=form, response=None)
        form.sender.data = DEFAULT_MAIL_SENDER
        form.valid_time.data = init_time()
        form.delayed_time.data = init_time(days=0)
        return render_template('index.html', operations=operations.Operations.operations(), form=form)
    return render_template('index.html', operations=operations.Operations.operations())
