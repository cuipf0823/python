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


class PlayerForm(FlaskForm):
    uid = IntegerField('Player uid', validators=[DataRequired()])
    channel = IntegerField('Player channel', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ServerForm(FlaskForm):
    server_id = SelectField('Select Query Server ID:', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(ServerForm, self).__init__(*args, **kwargs)
        self.server_id.choices = [(key, key) for key in OnlineServers.servers]


class MailReceiverForm(FlaskForm):
    receiver_type = RadioField(label='指定收件人类型')
    description = '注：1.全服发送， 无需填写； 2. 指定服发送，格式如：30000，30001; 3. 指定用户发送, 格式如：5000:0, 500100:0;'
    receive_info = StringField('收件人信息：', validators=[Regexp('^[0-9][0-9,:]*$', 0,
                                                            'receiver infomation must have only numbers,comma,colon.')],
                               description=description)

    def __init__(self, *args, **kwargs):
        super(MailReceiverForm, self).__init__(*args, **kwargs)
        self.receiver_type.choices = [(0, '全服发送'), (1, '指定服发送'), (2, '指定用户发送')]

    def validate_receive_info(self, field):
        rec_type = self.receiver_type.data
        if rec_type == 1:
            if ':' in field.data:
                raise ValidationError('receiver infomation format error.')


class MailForm(FlaskForm):
    title = StringField('邮件标题：', validators=[DataRequired(), Length(1, 64)])
    sender = StringField('发件人：', validators=[DataRequired(), Length(1, 32)])
    valid_time = DateTimeField('邮件有效时间(年-月-日 时:分:秒)', validators=[DataRequired(message='Invalid time.')])
    delayed_time = DateTimeField('邮件延时发送时间(年-月-日 时:分:秒)', validators=[DataRequired(message='Invalid time.')],
                                 description='无需延时，请勿调整')
    is_popping = BooleanField('新邮件是否弹出显示', validators=[DataRequired()])
    priority = BooleanField('新邮件是否置顶显示', validators=[DataRequired()])
    is_destory = BooleanField('邮件是否阅后即焚(带附件邮件勿勾选)', validators=[DataRequired()])
    mail_receiver = FormField(MailReceiverForm, label='收件人')
    attach = StringField('邮件附件：', validators=[Regexp('^[0-9][0-9,:]*$', 0,
                                                     'mail attachment must have only numbers,comma,colon.')],
                         description='邮件附件配置格式：item_id：num')
    content = TextAreaField('邮件内容：',  validators=[DataRequired(), Length(1, 1024)])
    submit = SubmitField('Send')

