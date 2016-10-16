#  coding:utf-8
'''
/***********************************************************
* Author       : M_Kepler
* EMail        : m_kepler@foxmail.com
* Last modified: 2016-10-16 10:00:09
* Filename     : emails.py
* Description  :
**********************************************************/
'''

from flask.ext.mail import Message
from threading import Thread
from app import app, mail


app.config['FLASK_MAIL_SUBJECT_PREFIX']='M_KEPLER'
app.config['FLASK_MAIL_SENDER']='M_KEPLER-m_kepler@foxmail.com'


def send_email(towho, subject, template, **kwargs):
    msg = Message(app.config['FLASK_MAIL_SUBJECT_PREFIX']+subject,
            sender = app.config['FLASK_MAIL_SENDER'], recipients=[towho])
    msg.body = render_template(template+'.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)

    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
