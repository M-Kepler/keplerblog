# -*- coding:utf-8 -*-

"""
用户角色表模型
"""

from ..plugins import db


class Role(db.Model):
    """
    表模型 - 用户角色
    """
    __tablename__ = 'roles'  # 指定表名
    id = db.Column(db.Integer, primary_key=True)  # 定义列对象
    name = db.Column(db.String(20), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    # users属性添加到Role模型中,用来返回与角色相关联的用户组成的列表,
    # 第一个参数表示这个关系的另一端是哪个模型
    # backref则表示向User模型添加一个role属性,
    # 从而定义反向关系，这个属性可替代role_id来访问Role表
    # lazy 指定如何加载相关记录

    @staticmethod
    def seed():
        # 调用这个方法就可以设置Role的默认值了
        db.session.add_all(
            map(lambda r: Role(name=r), ['administrators', 'guests']))
        db.session.commit()
