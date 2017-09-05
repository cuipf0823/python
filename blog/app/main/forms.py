# !/usr/bin/python
# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SelectField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from ..models import OnlineServers


class PlayerForm(FlaskForm):
    uid = StringField('Player uid', validators=[DataRequired()])
    channel = StringField('Player channel', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ServerForm(FlaskForm):
    server_id = SelectField('Select Query Server ID:', coerce=int)

    def __init__(self, *args, **kwargs):
        super(ServerForm, self).__init__(*args, **kwargs)
        self.server_id.choices = OnlineServers.servers

