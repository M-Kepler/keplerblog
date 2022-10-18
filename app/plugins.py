# -*- coding:utf-8 -*-

from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Separator
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
pagedown = PageDown()
login_manager = LoginManager()
nav = Nav()


def init_nav():
    # 初始化 导航栏
    nav_items = [
        View('HOME', 'main.index'),
        View('ARCHIVE', 'main.archive'),
    ]

    if current_user.is_administrator():
        nav_items.append(Subgroup(
            "MANAGE",
            View('NEW ARTICLE', 'main.edit'),
            View('ARTICLE MANAGE', 'main.edit'),
            View('CATEGORY MANAGE', 'main.edit')
        ))

    # 未登录用户
    if current_user.is_anonymoususer():
        nav_items.extend([
            View('SIGNUP', 'auth.signup'),
            View('SIGNIN', 'auth.signin')
        ])
    else:
        nav_items.append(Subgroup(
            current_user.name,
            View('SIGNOUT', 'auth.signout'),
            View('PROFILE', 'main.user', name=current_user.name)
        ))

    if not current_user.is_anonymoususer():
        nav_items.append(View('ABOUT', 'main.about'))

    nav.register_element(
        id='top', elem=Navbar('M_Kepler', *nav_items))
