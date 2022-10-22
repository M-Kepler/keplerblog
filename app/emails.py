# coding:utf-8

from threading import Thread

from flask import render_template
from flask_mail import Message

from flask import current_app
from .config import DevelopmentConfig as config
from .plugins import mail


def _send_async_email(msg):
    with current_app.app_context():
        mail.send(msg)


def send_email(towho, subject, template, **kwargs):
    msg = Message(config.FLASK_MAIL_SUBJECT_PREFIX + subject,
                  sender=config.FLASK_MAIL_SENDER,
                  recipients=[towho])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thread = Thread(target=_send_async_email, args=[app, msg])
    thread.start()
    return thread
