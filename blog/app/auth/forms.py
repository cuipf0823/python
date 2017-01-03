# !/usr/bin/python
# coding=utf-8

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import Regexp, EqualTo

from ..models import is_user_register, is_register


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 128), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    rem_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 128), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                         'Username must hava only '
                                                                                         'letters, numbers, '
                                                                                         'dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Password must'
                                                                                                  ' mathch.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    # 表单函数中定义了validate_开头的函数并且后面紧跟字段名的方法，这些方法
    # 会和常规的验证函数一起调用
    @staticmethod
    def validate_email(self, field):
        if is_register(field.data):
            raise ValidationError('Email already registered.')

    @staticmethod
    def validate_username(self, field):
        if is_user_register(field.data):
            raise ValidationError('Username already registered.')

