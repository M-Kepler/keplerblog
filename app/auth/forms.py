# coding:utf-8
from ..models import User
from flask_wtf import FlaskForm as Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, SubmitField, validators, ValidationError
from wtforms.validators import DataRequired, length, Regexp, EqualTo, Email


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
    remember_me = BooleanField('是否记住密码?', default = False)
    submit = SubmitField('登录')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise ValidationError('邮箱地址未注册')


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
    #  verification_code = StringField('验证码', validators=[
        #  DataRequired('此字段不能为空'),
        #  length(4,4,'填写4位验证码'),
        #  ])
    about_me= TextAreaField(label='关于我:')
    #  about_me= TextAreaField(label='关于我:', validators = [
        #  length(6,128,'长度必须在6-18之间')])
    submit = SubmitField("注册")

    #  自己定义校验,validatate_email 会自动被调用的
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱地址已注册')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('用户名已被注册')

class ResetPassword(Form):
    old_password = PasswordField(label='输入旧密码:', validators = [
        DataRequired('此字段不能为空'),
        length(6,128,'长度必须在6-18之间'),
        Regexp(r'^[a-zA-Z0-9_][a-zA-Z0-9]*$', 0, '密码只包含字母数字下划线'),
        ])
    new_password = PasswordField(label='输入新密码:', validators = [
        DataRequired('此字段不能为空'),
        length(6,128,'长度必须在6-18之间'),
        Regexp(r'^[a-zA-Z0-9_][a-zA-Z0-9]*$', 0, '密码只包含字母数字下划线'),
        ])
    new_password_again= PasswordField(label='再次输入密码:', validators = [
        DataRequired('此字段不能为空'),
        length(6,128,'长度必须在6-18之间'),
        Regexp(r'^[a-zA-Z0-9_][a-zA-Z0-9]*$', 0, '密码只包含字母数字下划线'),
        EqualTo('new_password', message='密码不一致')
        ])
    submit = SubmitField("更新密码")

class ForgetPassword(Form):
    pass
