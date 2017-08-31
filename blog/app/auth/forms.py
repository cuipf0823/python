# !/usr/bin/python
# coding=utf-8

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Length, Regexp


class LoginForm(FlaskForm):
    username = StringField('Account', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                        'Username must hava only ' 
                                                                                        'letters, numbers, '
                                                                                        'dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired()])
    # rem_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')







