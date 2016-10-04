# coding:utf-8
#  并不需要这句
#  import mysql.connector
from . import db # 当前包引入


'''
#  定义模型
class Role(db.Model):
    __tablename__='roles' # 指定表名
    role_id = db.Column(db.Integer, primary_key = True) # 定义列对象
    user_name = db.Column(db.String, nullable = False)
    user_password = db.Column(db.String, nullable = False)
    #  建立两表间关系，backref是定义反向关系
    users = db.relationship('User', backref = 'roles')

    def __repr__(self):
        #  进行测试时方便查看
        #  return '<Role {}>'.format(self.name)
        return '<Role %r>' % self.name
'''

class User(db.Model):
    __tablename__='users'
    user_id = db.Column(db.Integer, primary_key = True) # 主键
    user_name = db.Column(db.String(20))
    user_passwd = db.Column(db.String(20))

    def __init__(self, user_id, user_name, user_passwd):
        self.user_id = user_id
        self.user_name = user_name
        self.user_passwd = user_passwd

    def __str__(self):
        return 'user_id:{}\tuser_name:{}\tuser_passwd:{}'.format(self.user_id, self.user_name, self.user_passwd)

    #  def __repr__(self):
        #  return '<User %r>' % self.name



