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

from flask import Flask, request
from werkzeug.routing import BaseConverter
from flask.ext.mail import Mail
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

#  from flask.ext.nav import Nav
#  from flask_nav.elements import *


from os import path
from datetime import datetime
from .config import config
#  from .views import init_views 以前是通过文件导入，现在选择注册蓝图


#  为路由规则增加正则转换器
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex=items[0]



#  应用这个导航栏插件就不需要自己写导航栏了,
#  可以用操作对象的形式来设置导航栏 #  注册到导航栏对象top

#  nav = Nav()

bootstrap = Bootstrap()
db = SQLAlchemy()
#  manager = Manager()
moment=Moment()
mail=Mail()

login_manager = LoginManager()
login_manager.session_protection='strong'
#  login_manager.session_protection='basic'
login_manager.login_view = 'auth.signin'

basedir = path.abspath(path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter
    #  初始化

    #  nav.register_element('top', Navbar('M_Kepler',
        #  View('Home', 'main.index'),
        #  Subgroup(
            #  'Products',
            #  View('Projects', 'main.projects'),
            #  Separator(),
            #  View('Archive', 'main.archive'),
            #  ),
        #  View('Signup', 'auth.signup'),
        #  View('Signin', 'auth.signin'),
        #  View('Signout', 'auth.signout'),
        #  View('About', 'main.about'),
    #  ))

    #  app.config.from_pyfile('config.py')
    app.config.from_object(config['default'])

    #  nav.init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    #  init_views(app)
    # 注册蓝图
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    #  url_prefix(url前缀)加上后就把auth目录下的view注册到蓝图中，不加的话就使用app下的view
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    #  static_fold  指定蓝图的静态文件所在文件夹
    #  app.register_blueprint(main_blueprint, url_prefix='/main', static_fold='static')
    app.register_blueprint(main_blueprint, static_fold='static')

    @app.template_test('current_link')
    def is_current_link(link):
        return link == request.path

    return app

