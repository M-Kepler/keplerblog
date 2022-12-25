# _*_coding:utf-8_*_

"""
/***********************************************************
* Author       : M_Kepler
* EMail        : hellohuangjinjie@gmail.com
* Last modified: 2016-10-01 10:09:58
* Filename     : app.py
* Description  :
**********************************************************/
"""

from flask import Flask, request
from werkzeug.routing import BaseConverter

from .config import config_map
from .hook import init_hook
from .plugins import bootstrap, db, login_manager, mail, moment, nav, pagedown


class RegexConverter(BaseConverter):
    """
    为路由规则增加正则转换器
    """

    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def _load_plugins(app):
    """
    应用这个导航栏插件就不需要自己写导航栏了,
    可以用操作对象的形式来设置导航栏 # 注册到导航栏对象top
    """

    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.signin'

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    nav.init_app(app)


def _load_config(app):
    """
    加载配置
    """
    # app.config.from_pyfile('config.py')
    app.config.from_object(config_map['default'])


def _init_blueprint(app):
    """
    # 注册蓝图
    """
    # from .views import init_views 以前是通过文件导入，现在选择注册蓝图
    # init_views(app)

    from .auth.views import auth as auth_blueprint
    from .main.views import main as main_blueprint

    # url_prefix 既可以放在定义，也可以放在注册时候，非常方便
    # url_prefix(url前缀) 加上后就把 auth 目录下的 view 注册到蓝图中，不加的话就使用 app 下的 view
    # static_fold  指定蓝图的静态文件所在文件夹
    app.register_blueprint(main_blueprint, static_fold='static')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')


def create_app():
    """
    服务启动时，实例化一次
    算是 flask 的一种设计规范吧，主要还是为了解决循环引用的问题
    """

    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter

    # 添加路由前缀
    # FIXME 这种方式会导致请求静态资源的时候，访问的也是加了前缀后的 URL
    # 例如: http://localhost:5000/kepler/assets/css/bootstrap-responsive.css
    # from .utils.middlewares import PrefixMiddleware
    # app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=Config.URL_PREFIX)

    # 初始化配置
    _load_config(app)

    # 初始化插件
    _load_plugins(app)

    # 初始化蓝图
    _init_blueprint(app)

    @app.template_test('current_link')
    def is_current_link(link):
        return link == request.path

    init_hook(app)
    print(app.url_map)

    return app
