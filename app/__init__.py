#_*_coding:utf-8_*_
'''
/***********************************************************
* Author       : M_Kepler
* EMail        : hellohuangjinjie@gmail.com
* Last modified: 2016-10-01 10:09:58
* Filename     : app.py
* Description  :
**********************************************************/
'''

from flask import Flask
#  from flask import Flask, flash, session, request, render_template, url_for, redirect, abort, current_app
from werkzeug.routing import BaseConverter

from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.nav import Nav
from flask_nav.elements import *

from os import path
from datetime import datetime

from .views import init_views


#  为路由规则增加正则转换器
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex=items[0]



#  应用这个导航栏插件就不需要自己写导航栏了,
#  可以用操作对象的形式来设置导航栏 #  注册到导航栏对象top
nav = Nav()
bootstrap = Bootstrap()
db = SQLAlchemy()
#  manager = Manager()
moment=Moment()
basedir = path.abspath(path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter
    #  初始化
    nav.register_element('top', Navbar('M_Kepler',
        View('Home', 'home'),
        Subgroup(
            'Products',
            View('Upload', 'upload'),
            ),
        View('Projects', 'projects'),
        View('Archive', 'archive'),
        View('Login', 'login'),
        View('Signin', 'signin'),
        View('Signout', 'signout'),
        View('About', 'about'),
    ))
    app.config.from_pyfile('config')
    nav.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    #  manager = Manager(app)
    #  moment.init_app(app)
    init_views(app)
    return app

