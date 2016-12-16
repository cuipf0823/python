# !/usr/bin/python
# coding=utf-8
from flask import session
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from forms import NameForm
from ..models import check_name
from . import blue
from .. import email


# 检测输入用户是否在数据库中
@blue.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('looks like you changed your name!')
        session['name'] = form.name.data
        if len(check_name(form.name.data)) == 0:
            session['exist'] = False
            flash('you name not in sql')
        else:
            session['exist'] = True
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'), exist=session.get('exist'))