# !/usr/bin/python
# coding=utf-8

from threading import Thread
from flask import current_app
from flask import render_template
from flask_mail import Message
from . import mail


def send_sync_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['MAIL_SENDER'], recipients=[to])
    print app.config['MAIL_SUBJECT_PREFIX'] + subject
    print app.config['MAIL_SENDER']
    print to
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thread = Thread(target=send_sync_mail, args=[app, msg])
    thread.start()
    send_sync_mail(app, msg)
