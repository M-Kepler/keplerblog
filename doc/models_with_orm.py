# coding:utf-8

#  import mysql.connector

from app import db


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    #  相当于varchar(20)
    user_name = db.Column(db.String(20))
    user_passwd = db.Column(db.String(20))

    def __init__(self, user_id, user_name, user_passwd):
        self.user_id = user_id
        self.user_name = user_name
        self.user_passwd = user_passwd

    def __str__(self):
        return 'user_id:{}\tuser_name:{}\tuser_passwd:{}'.format(self.user_id, self.user_name, self.user_passwd)

    def _repr__(self):
        return '<User %r>' % self.user_name
