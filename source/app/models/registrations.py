# -*- coding:utf-8 -*-

"""
中间表
"""

from ..plugins import db

registrations = db.Table(
    'registrations', db.Column('post_id', db.Integer, db.ForeignKey('posts.id')),
    db.Column('category_id.id', db.Integer, db.ForeignKey('categorys.id')))
