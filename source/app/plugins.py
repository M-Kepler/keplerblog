# -*- coding:utf-8 -*-

"""
Flask 插件
"""

from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_nav import Nav
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
pagedown = PageDown()
login_manager = LoginManager()
nav = Nav()
