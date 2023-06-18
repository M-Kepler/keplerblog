# -*- coding:utf-8 -*-

"""
用户表模型
"""

from datetime import datetime

from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous import Serializer
from werkzeug.security import check_password_hash, generate_password_hash

from ..plugins import db, login_manager
from .role import Role


class User(db.Model, UserMixin, AnonymousUserMixin):
    """
    表模型 - 用户
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    passwd_hash = db.Column(db.String(128))
    register_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)  # 是否确认了邮箱验证
    about_me = db.Column(db.Text())
    role_id = db.Column(db.Integer,
                        db.ForeignKey('roles.id'))  # 表示该列的值是role表的id

    posts = db.relationship('Post', backref='author')
    comments = db.relationship('Comment', backref='author')

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def is_anonymoususer(self):
        return False

    def is_administrator(self):
        if (self.role.name == 'administrators'):
            return True
        else:
            return False

    @staticmethod
    def on_created(target, value, oldvalue, initiator):
        target.role = Role.query.filter_by(name='guests').first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, passwd):
        """
        user.password=''  # 设置存入生成的散列密码
        user.varify_password(passwd)  # 来校验密码
        """
        self.passwd_hash = generate_password_hash(passwd)

    def verify_password(self, passwd):
        return check_password_hash(self.passwd_hash, passwd)

    def generate_confirmation_token(self, expiration=3600):
        """
        根据用户id吧生成一个token然后包装发给用户邮箱，如果有人点击了就可以确认了-
        生成一个有效期为1小时的token（令牌）
        """

        s = Serializer(current_app.config['SECRET_KEY'],
                       expiration)  # 根据秘钥SECRET_KEY,生成一个会过期的JSON
        return s.dumps({'confirm': self.id})  # 看过序列化和反序列化都知道

    def confirm(self, token):
        """
        校验这个token
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        # 将confirmed加到User对象中,这里我感觉是需要commit的,但是记得吗?commit_on_tearndown
        db.session.add(self)
        # db.session.commit()
        return True

    @staticmethod
    def generate_fake(count=20):
        """
        用 foregy 生成测试数据
        """

        from random import seed

        import forgery_py
        from sqlalchemy.exc import IntegrityError
        seed()
        for i in range(count):
            u = User(name=forgery_py.internet.user_name(True),
                     email=forgery_py.internet.email_address(),
                     passwd_hash=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     register_time=forgery_py.date.date(True))
            db.session.add(u)
            # 随机生成的这些信息可能会重复导致session.commit跑出异常
            # 所以回滚回话撤销之前的操作，重新生成就可以了
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class AnonymousUser(AnonymousUserMixin):
    """
    表模型 - 匿名用户
    """
    @property
    def locale(self):
        return 'zh'

    def is_anonymoususer(self):
        return True

    # 如果我使用默认的AnonymousUserMixin的话,
    # 在判断是不是administrator该不该显示删除修改按钮的时候就会出错
    # 因为没有is_administrator这个方法
    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    """
    用户的回调函数
    把已经登录的用户id放到session里,告诉flask-login怎么看哪些用户已经登录,
    然后其他地方需要的时候可以直接通过current_user来获取当前登录用户的信息,如:current_user.name
    login_manager验证用户登录成功后会派发cookie到浏览器，用户访问另一个页面的时候
    会读取这个cookie, 实际上这个cookie存的就是这个id
    """
    return User.query.get(int(user_id))


# 数据库on_created事件监听
# 每插入新对象就初始化用户的Role_id为guests
db.event.listen(
    User.name, 'set', User.on_created)
