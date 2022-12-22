# -*- coding:utf-8 -*-

"""
请求 / 响应钩子

"""

from .plugins import nav
from flask_login import current_user
from flask_nav.elements import Navbar, Subgroup, View


def init_hook(app):
    """
    钩子
    """

    @app.before_request
    def test():
        print("-" * 40)

    @app.before_request
    def init_nav():
        """
        初始化导航栏
        FIXME 每次请求都初始化也不好
        """
        nav_items = [
            View("HOME", "main.home"),
            View("ARCHIVE", "main.archive_view"),
        ]

        if current_user.is_administrator():
            nav_items.append(Subgroup(
                "MANAGE",
                # FIXME 这里还必须带一个参数，否则编辑文章的时候会报错
                View("NEW ARTICLE", "main.edit_post_view", post_id=0),
                View("ARTICLE MANAGE", "main.home"),
                View("CATEGORY MANAGE", "main.home")
            ))

        # 未登录用户
        if current_user.is_anonymoususer():
            nav_items.extend([
                View("SIGNUP", "auth.signup"),
                View("SIGNIN", "auth.signin")
            ])
        else:
            nav_items.append(Subgroup(
                current_user.name,
                View("SIGNOUT", "auth.signout"),
                View("PROFILE", "main.user_view", name=current_user.name)
            ))

        if not current_user.is_anonymoususer():
            nav_items.append(View("ABOUT", "main.about_view"))

        nav.register_element(
            id="top", elem=Navbar("M_Kepler", *nav_items))
