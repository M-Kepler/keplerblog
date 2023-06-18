# coding:utf-8

"""
文章分类表模型
"""


from ..plugins import db


class Category(db.Model):
    """
    表模型 - 类别
    """
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    @staticmethod
    def seed():
        db.session.add_all(
            map(lambda r: Category(name=r), ['others', 'python', 'linux']))
        db.session.commit()

    @staticmethod
    def generate_fake(count=20):
        from random import seed

        import forgery_py
        seed()
        for i in range(count):
            c = Category(name=forgery_py.internet.user_name(True))
            db.session.add(c)
