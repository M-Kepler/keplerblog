#  coding:utf-8
from flask import render_template
from flask_mail import Message
from threading import Thread
from . import create_app, mail
from .config import DevelopmentConfig as config

app = create_app()

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(towho, subject, template, **kwargs):
    msg = Message(config.FLASK_MAIL_SUBJECT_PREFIX+subject,
            sender = config.FLASK_MAIL_SENDER ,recipients=[towho])
    msg.body = render_template(template+'.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread


