# coding:utf-8
from ..models import User
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, SubmitField, validators
from wtforms.validators import DataRequired, length, Regexp, EqualTo, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class LoginForm(Form):
    email = StringField(label='电子邮箱:', validators = [
        DataRequired('此字段不能为空'),
        length(6,64,'长度必须在6-64之间'),
        Email('邮箱格式有误')
        ])
    password = PasswordField(label='密码:', validators = [
        DataRequired(),
        length(6,128,'长度必须在6-18之间'),
        Regexp(r'^[a-zA-Z0-9_][a-zA-Z0-9]*$', 0, '密码只包含字母数字下划线')
        ])
    remeber_me = BooleanField('是否记住密码?', default = False)
    submit = SubmitField('登录')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise alidationError('邮箱地址未注册')


class RegForm(Form):
    username = StringField(label='用户名:', validators = [
        DataRequired('用户名不能为空'), length(6,18,'长度必须在6-18之间')
        #  Regexp('^[A-Za-z][A-Za-z0-9_.]$', 0, "用户名只允许字母数字下划线")
        ])
    email = StringField(label='电子邮箱:', validators = [
        DataRequired('此字段不能为空'),
        length(6,64,'长度必须在6-64之间'),
        Email('邮箱格式有误')
        ])
    password = PasswordField(label='密码:', validators = [
        DataRequired('此字段不能为空'),
        length(6,128,'长度必须在6-18之间'),
        Regexp(r'^[a-zA-Z0-9_][a-zA-Z0-9]*$', 0, '密码只包含字母数字下划线')
        ])
    password_again = PasswordField(label='再次输入密码:', validators = [
        DataRequired('此字段不能为空'),
        length(6,128,'长度必须在6-18之间'),
        Regexp(r'^[a-zA-Z0-9_][a-zA-Z0-9]*$', 0, '密码只包含字母数字下划线'),
        EqualTo('password', message='密码不一致')
        ])
    submit = SubmitField("注册")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise alidationError('邮箱地址已注册')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise alidationError('用户名已被注册')




'''
class PostArticleForm(Form):
    title = StringField("标题", validators = [Required(), length(6, 64)])
    body = TextAreaField("内容")
    category_id = QuerySelectField("分类", query_factory = lambda:Category.query.all(),
            get_pk = lambda a:str(a.id), get_label = lambda a:a.name)
    submit = StringField("发布")
    '''

