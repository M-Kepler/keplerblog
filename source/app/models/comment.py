# -*- coding:utf-8 -*-

"""
文章评论表模型
"""


from datetime import datetime

from markdown import markdown
from ..plugins import db
from .user import User
from .post import Post


class Comment(db.Model):
    """
    表模型 - 评论
    """
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)  # 把markdown原文格式成html存到数据库，而不是访问时在格式
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'))  # 表示该列的值是posts表的id

    @staticmethod
    def on_body_changed(target, value, oldvalue, initiator):
        if value is None or (value == ''):
            target.body_html = ''
        else:
            target.body_html = markdown(value)

    @staticmethod
    def generate_fake(count=100):
        from random import randint, seed

        import forgery_py
        seed()
        user_count = User.query.count()
        post_count = Post.query.count()
        for i in range(count):
            p = Post.query.offset(randint(0, post_count - 1)).first()
            u = User.query.offset(randint(0, user_count - 1)).first()
            Comment(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                    create_time=forgery_py.date.date(True),
                    author=u,
                    post=p)


# 当 body 被修改时触发
db.event.listen(
    Comment.body, 'set', Comment.on_body_changed)
