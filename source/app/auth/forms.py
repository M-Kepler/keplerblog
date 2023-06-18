# coding:utf-8

"""
auth 模块的表单
"""

from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, StringField, SubmitField,
                     TextAreaField, ValidationError)
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, length

from ..models.user import User


class LoginForm(FlaskForm):
    """
    表单 - 登录
    """
    email = StringField(label='电子邮箱:',
                        validators=[
                            DataRequired('此字段不能为空'),
                            length(6, 64, '长度必须在6-64之间'),
                            Email('邮箱格式有误')
                        ])
    password = PasswordField(label='密码:',
                             validators=[
                                 DataRequired(),
                                 length(6, 128, '长度必须在6-18之间'),
                                 Regexp(r'^[a-zA-Z0-9_][a-zA-Z0-9]*$', 0,
                                        '密码只包含字母数字下划线')
                             ])
    remember_me = BooleanField('是否记住密码?', default=False)
    submit = SubmitField('登录')

    def validate_email(self, field):
        """
        检查邮箱
        validate_$form_name 会自动被调用的
        """
        user = User.query.filter_by(email=field.data).first()
        if not user:
            raise ValidationError('邮箱地址未注册')


class RegForm(FlaskForm):
    """
    表单 - 注册
    """
    username = StringField(
        label='用户名:',
        validators=[
            DataRequired('用户名不能为空'),
            length(6, 18, '长度必须在6-18之间')
            # Regexp('^[A-Za-z][A-Za-z0-9_.]$', 0, "用户名只允许字母数字下划线")
        ])
    email = StringField(label='电子邮箱:',
                        validators=[
                            DataRequired('此字段不能为空'),
                            length(6, 64, '长度必须在6-64之间'),
                            Email('邮箱格式有误')
                        ])
    password = PasswordField(label='密码:',
                             validators=[
                                 DataRequired('此字段不能为空'),
                                 length(6, 128, '长度必须在6-18之间'),
                                 Regexp(r'^[a-zA-Z0-9_][a-zA-Z0-9]*$', 0,
                                        '密码只包含字母数字下划线')
                             ])
    password_again = PasswordField(label='再次输入密码:',
                                   validators=[
                                       DataRequired('此字段不能为空'),
                                       length(6, 128, '长度必须在6-18之间'),
                                       Regexp(r'^[a-zA-Z0-9_][a-zA-Z0-9]*$', 0,
                                              '密码只包含字母数字下划线'),
                                       EqualTo('password', message='密码不一致')
                                   ])
    # 验证码
    """
    verification_code = StringField(label='验证码',
                                    validators=[
                                        DataRequired('此字段不能为空'),
                                        length(4,4,'填写4位验证码'),
                                    ])
    """
    about_me = TextAreaField(label='关于我:')
    submit = SubmitField("注册")

    def validate_email(self, field):
        """
        自己定义校验
        """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱地址已注册')

    def validate_username(self, field):
        """
        校验用户名
        """
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('用户名已被注册')


class ResetPassword(FlaskForm):
    """
    表单 - 密码重置
    """
    old_password = PasswordField(label='输入旧密码:',
                                 validators=[
                                     DataRequired('此字段不能为空'),
                                     length(6, 128, '长度必须在6-18之间'),
                                     Regexp(r'^[a-zA-Z0-9_][a-zA-Z0-9]*$', 0,
                                            '密码只包含字母数字下划线'),
                                 ])
    new_password = PasswordField(label='输入新密码:',
                                 validators=[
                                     DataRequired('此字段不能为空'),
                                     length(6, 128, '长度必须在6-18之间'),
                                     Regexp(r'^[a-zA-Z0-9_][a-zA-Z0-9]*$', 0,
                                            '密码只包含字母数字下划线'),
                                 ])
    new_password_again = PasswordField(label='再次输入密码:',
                                       validators=[
                                           DataRequired('此字段不能为空'),
                                           length(6, 128, '长度必须在6-18之间'),
                                           Regexp(
                                               r'^[a-zA-Z0-9_][a-zA-Z0-9]*$',
                                               0, '密码只包含字母数字下划线'),
                                           EqualTo('new_password',
                                                   message='密码不一致')
                                       ])
    submit = SubmitField("更新密码")

