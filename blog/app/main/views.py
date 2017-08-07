# !/usr/bin/python
# coding=utf-8
from flask import render_template
from flask import redirect, url_for, flash
from flask_login import login_required
from flask_login import current_user
from . import main
from ..models import get_user_by_name, update_frofile
from .forms import EditProfileForm


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user_info = get_user_by_name(username)
    if user_info is None:
        abort(404)
    print(type(user_info.last_seen))
    print(user_info.last_seen)
    return render_template('user.html', user=user_info)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        # 更新数据库
        update_frofile(current_user.id, current_user.username, current_user.location, current_user.about_me)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.username
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)
