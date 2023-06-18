# coding:utf-8

"""
文章表模型
"""

from datetime import datetime

import bleach
from markdown import markdown
from sqlalchemy import extract

from ..plugins import db
from .registrations import registrations
from .category import Category
from .user import User


class Post(db.Model):
    """
    表模型 - 文章
    """
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)  # 把markdown原文格式成html存到数据库，而不是访问时在格式
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    comments = db.relationship('Comment', backref='post')
    read_count = db.Column(db.Integer, default=0)
    private = db.Column(db.Boolean, default=False)

    # TODO 多对多
    # category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
    categorys = db.relationship('Category',
                                secondary=registrations,
                                backref=db.backref('posts', lazy='dynamic'),
                                lazy='dynamic')

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def on_body_changed(target, value, oldvalue, initiator):
        """
        MySQL 触发器，当 body 列数据发生变化时触发
        """
        target.category = Category.query.filter_by(name='others').first()
        allow_tags = [
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li',
            'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p', 'img'
        ]
        # 转换 markdown 为 html , 并清洗 html 标签
        if value is None or (value == ''):
            target.body_html = ''
        else:
            target.body_html = bleach.linkify(
                bleach.clean(
                    markdown(value, output_form='html'),
                    tags=allow_tags,
                    strip=True,
                    attributes={
                        '*': ['class'],
                        'a': ['href', 'rel'],
                        'img': ['src', 'alt'],  # 支持<img src …>标签和属性
                    }))

    @staticmethod
    def generate_fake(count=100):
        """
        生成测试数据
        """
        from random import randint, seed

        import forgery_py
        seed()
        user_count = User.query.count()
        category_count = Category.query.count()
        for _ in range(count):
            # offset 查询过滤器会跳过参数中指定的查询数量<通过设定一个随机的偏移值
            # 调用 first() 来使得每次获取到一个不同的随机用户
            category_1 = Category.query.offset(
                randint(0, category_count - 1)).first()
            category_2 = Category.query.offset(
                randint(0, category_count - 1)).first()
            u = User.query.offset(randint(0, user_count - 1)).first()
            Post(categorys=[category_1, category_2],
                 title=forgery_py.lorem_ipsum.title(randint(1, 3)),
                 body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                 create_time=forgery_py.date.date(True),
                 author=u,
                 read_count=randint(1, 10000))

    def getdate(self):
        data = db.session.query(
            extract('month', self.create_time).label('month')).first()
        return data[0]
        # return db.func.extract('month', self.create_time)


# 当 body 被修改时触发
db.event.listen(
    Post.body, 'set', Post.on_body_changed)
