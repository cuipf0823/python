# !/usr/bin/python
# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SelectField
from wtforms import SubmitField
from wtforms import DateTimeField
from wtforms import BooleanField
from wtforms import FormField
from wtforms import RadioField
from wtforms import IntegerField
from wtforms import TextAreaField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Regexp
from ..models import OnlineServers
import logging


class PlayerForm(FlaskForm):
    uid = IntegerField('Player uid:', validators=[DataRequired(message='uid must have only numbers.')],
                       description='player must be online.')
    channel = IntegerField('Player channel:')
    submit = SubmitField('Submit')


class DelMailForm(FlaskForm):
    mail_id = IntegerField('Delete unsend mail id:', validators=[DataRequired(message='mail id must have only numbers.')])
    submit = SubmitField('Submit')


class RoomInfoForm(FlaskForm):
    server_id = SelectField('Server id:', coerce=int)
    room_id = StringField('Room id：', validators=[Regexp('^[0-9]*$', 0, 'room id must have only numbers.')])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(RoomInfoForm, self).__init__(*args, **kwargs)
        self.server_id.choices = [(key, key) for key in OnlineServers.servers]


class ServerForm(FlaskForm):
    server_id = SelectField('Select Query Server ID:', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(ServerForm, self).__init__(*args, **kwargs)
        self.server_id.choices = [(key, key) for key in OnlineServers.servers]


class MailReceiverForm(FlaskForm):
    receiver_type = RadioField(label='指定收件人类型', coerce=int, default=0)
    description = '注：1.全服发送，无需填写； 2. 指定服发送,格式如:online_id,online_id; ' \
                  '3. 指定用户发送, 格式如：online_id:uid,uid'
    receive_info = StringField('收件人信息：', validators=[Regexp('[0-9,:]*$', 0,
                                                            'receiver infomation must have only numbers,comma,colon.')],
                               description=description)

    def __init__(self, *args, **kwargs):
        super(MailReceiverForm, self).__init__(*args, **kwargs)
        self.receiver_type.choices = [(0, '全服发送'), (1, '指定服发送'), (2, '指定用户发送')]

    def validate_receive_info(self, field):
        rec_type = self.receiver_type.data
        if rec_type >= 1 and len(field.data) == 0:
            raise ValidationError('receiver infomation format error.')
        if rec_type == 1:
            try:
                online_ids = [int(item) for item in field.data.split(',')]
                logging.debug('validate receiver infomation receive_type:{0} online_ids:{1}'.format(
                    rec_type, online_ids))
            except BaseException:
                raise ValidationError('receiver infomation format error.')
        elif rec_type == 2:
            try:
                infomations = field.data.split(':')
                online_id = int(infomations[0])
                uids = [int(item) for item in infomations[1].split(',')]
                logging.debug('validate receiver infomation receive_type:{0} online_id:{1} uids:{2}'.format(
                    rec_type, online_id, uids))
            except BaseException:
                raise ValidationError('receiver infomation format error.')


class MailForm(FlaskForm):
    title = StringField('邮件标题：', validators=[DataRequired(), Length(1, 64)])
    sender = StringField('发件人：', validators=[DataRequired(), Length(1, 32)])
    valid_time = DateTimeField('邮件有效时间(年-月-日 时:分:秒)', validators=[DataRequired(message='Invalid time.')])
    delayed_time = DateTimeField('邮件延时发送时间(年-月-日 时:分:秒)', validators=[DataRequired(message='Invalid time.')],
                                 description='无需延时，请勿调整')
    is_popping = BooleanField('新邮件是否弹出显示')
    priority = BooleanField('新邮件是否置顶显示')
    is_destory = BooleanField('邮件是否阅后即焚(带附件邮件勿勾选)')

    mail_receiver = FormField(MailReceiverForm, label='收件人')
    attach = StringField('邮件附件：', validators=[Regexp('[0-9,:]*$', 0,
                                                     'mail attachment must have only numbers,comma,colon.')],
                         description='邮件附件配置格式：item_id：num')
    content = TextAreaField('邮件内容：',  validators=[DataRequired(), Length(1, 1024)])
    submit = SubmitField('Send')

    def validate_attach(self, field):
        if len(field.data) != 0:
            try:
                attachs = [item.split(':') for item in field.data.split(',')]
                attachments = [(int(item[0]), int(item[1])) for item in attachs]
                logging.debug('validate mail attachments {}'.format(attachments))
            except BaseException:
                raise ValidationError('mail attachment format error')

