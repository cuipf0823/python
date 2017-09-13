# !/usr/bin/python
# coding=utf-8
from flask import render_template
from flask import redirect, url_for, abort
from flask_login import current_user, login_required
from . import main
from ..models import UserManager
from ..models import query_operators, query_callback
from ..models import query_response_cb, callback_type
from .forms import PlayerForm, ServerForm, MailForm
from .forms import DelMailForm, RoomInfoForm
import logging
import datetime

DEFAULT_MAIL_SENDER = '纸盒人星球官方'


def init_time(days=15):
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=days)
    valid_time = now + delta
    return valid_time


def calc_second(dt_time):
    # return time.mktime(time.strptime(str_time, '%Y-%m-%d %H:%M:%S')) - time.time()
    return int((dt_time - datetime.datetime.now()).total_seconds())


def handle_query_mail(form):
    mail_info = {}
    mail_info.setdefault('title', form.title.data)
    mail_info.setdefault('sender', form.sender.data)
    mail_info.setdefault('content', form.content.data)
    mail_info.setdefault('valid_time', calc_second(form.valid_time.data))
    delayed_time = calc_second(form.delayed_time.data)
    if delayed_time > 0:
        mail_info.setdefault('delayed_time', delayed_time)
    else:
        mail_info.setdefault('delayed_time', 0)
    mail_info.setdefault('is_popping', form.is_popping.data)
    mail_info.setdefault('priority', form.priority.data)
    mail_info.setdefault('is_destory', form.is_destory.data)
    receive_type = form.mail_receiver.data.get('receiver_type')
    mail_info.setdefault('receive_type', receive_type)
    if receive_type == 1:
        online_ids = [int(item) for item in form.mail_receiver.data.get('receive_info').split(',')]
        mail_info.setdefault('receive_onlines', online_ids)
    elif receive_type == 2:
        infomations = form.mail_receiver.data.get('receive_info').split(':')
        online_id = int(infomations[0])
        uids = [int(item) for item in infomations[1].split(',')]
        mail_info.setdefault('receive_online', online_id)
        mail_info.setdefault('receive_uids', uids)
    if not form.is_destory.data and form.attach.data:
        attachs = [item.split(':') for item in form.attach.data.split(',')]
        attachments = [(int(item[0]), int(item[1])) for item in attachs]
        mail_info.setdefault('attachments', attachments)
    mail_info.setdefault('content', form.content.data)
    return mail_info


def query_param_none(opt):
    ret = query_callback(opt, current_user)
    if ret.status_code == 0:
        # 更新内存数据
        query_response_cb(opt, ret.response)
    return render_template('index.html', operations=query_operators(), response=str(ret.response))


def query_param_uid_channel(opt):
    form = PlayerForm()
    if form.validate_on_submit():
        uid = form.uid.data
        channel = form.channel.data
        logging.debug('query {0} from gm server uid: {1}, channel: {2}'.format(opt, uid, channel))
        ret = query_callback(opt, current_user, uid=uid, channel=channel)
        return render_template('index.html', operations=query_operators(), form=form, response=str(ret.response))
    form.channel.data = 0
    return render_template('index.html', operations=query_operators(), form=form)


def query_param_server(opt):
    form = ServerForm()
    if form.validate_on_submit():
        server_id = form.server_id.data
        ret = query_callback(opt, current_user, server_id=server_id)
        return render_template('index.html', operations=query_operators(), form=form, response=str(ret.response))
    return render_template('index.html', operations=query_operators(), form=form)


def query_param_mail(opt):
    form = MailForm()
    if form.validate_on_submit():
        mail_info = handle_query_mail(form)
        logging.debug(mail_info)
        ret = query_callback(opt, current_user, mail_info=mail_info)
        return render_template('index.html', operations=query_operators(), form=form, response=str(ret.response))
    form.sender.data = DEFAULT_MAIL_SENDER
    form.valid_time.data = init_time()
    form.delayed_time.data = init_time(days=0)
    form.mail_receiver.data.setdefault('receiver_type', 1)
    return render_template('index.html', operations=query_operators(), form=form)


def query_param_mail_id(opt):
    form = DelMailForm()
    if form.validate_on_submit():
        mail_id = form.mail_id.data
        logging.info('delete unsend mail mail_id: {}'.format(mail_id))
        ret = query_callback(opt, current_user, mail_id=mail_id)
        return render_template('index.html', operations=query_operators(), form=form, response=str(ret.response))
    return render_template('index.html', operations=query_operators(), form=form)


def query_param_room_info(opt):
    form = RoomInfoForm()
    if form.validate_on_submit():
        server_id = form.server_id.data
        room_id = int(form.room_id.data)
        ret = query_callback(opt, current_user, server_id=server_id, room_id=room_id)
        return render_template('index.html', operations=query_operators(), form=form, response=str(ret.response))
    return render_template('index.html', operations=query_operators(), form=form)


# 根据不同类返回不同的视图函数
query_func = {callback_type().PARAM_NONE: query_param_none,
              callback_type().PARAM_UID_CHANNEL: query_param_uid_channel,
              callback_type().PARAM_SERVER_ID: query_param_server,
              callback_type().PARAM_MAIL: query_param_mail,
              callback_type().PARAM_MAIL_ID: query_param_mail_id,
              callback_type().PARAM_ROOM_INFO: query_param_room_info
              }


@main.route('/query/<int:param_type>/<opt>', methods=['GET', 'POST'])
@login_required
def query(param_type, opt):
    logging.debug('query {0} from gm server type: {1}'.format(opt, param_type))
    func = query_func.get(param_type, None)
    if func:
        return func(opt)
    return render_template('index.html', operations=query_operators())


@main.before_request
def before_request():
    """
    print(tcp_connect.is_connect)
    if not tcp_connect.is_connect:
        flash('Connect GM server failed, please login again.')
        logging.error('Connect GM server failed, please login again.')
    if OnlineServers.last_time == 0:
        opt = 'list'
        operations.Operations.callback(opt)
    """


@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', operations=query_operators())
    return redirect(url_for('auth.login'))


@main.route('/user/<user_id>')
@login_required
def user(user_id):
    user_info = UserManager.get_user_by_id(int(user_id))
    if user_info is None:
        abort(404)
    return render_template('user.html', user=user_info)
