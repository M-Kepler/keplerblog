# coding:utf-8

"""
表单
"""

from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm as Form
from wtforms import (BooleanField, SelectField, StringField, SubmitField,
                     TextAreaField, ValidationError)
from wtforms.validators import DataRequired, Email, Regexp, length

from ..models import Category, Role, User


class PostForm(Form):
    """
    表单 - 文章主体
    """
    title = StringField(label=('标题'), validators=[DataRequired()])
    category = StringField("分类", validators=[DataRequired()])
    body = PageDownField(label=('正文'), validators=[DataRequired()])
    private = BooleanField("私人")
    # render_kw 参数，设置标签属性，方便 js 操作，例如根据 id 取值，绑定 onchange 事件等
    submit = SubmitField('提交', render_kw={'id': 'submit_by_kw'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 下拉的多选框必须是 tuple 类型，第一个元素为值，第二个元素为展示内容
        self.category.choices = [
            (category.id, category.name)
            for category in Category.query.order_by(Category.name).all()
        ]


class AddCategoryForm(Form):
    """
    表单 - 添加分类
    """
    categoryname = StringField('新分类',
                               validators=[DataRequired(),
                                           length(1, 64)])
    submit = SubmitField('添加')

    def validate_categoryname(self, field):
        """
        分类名校验
        """
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('分类已存在')


class CommentForm(Form):
    """
    表单 - 评论
    """
    body = PageDownField(label=('Comment'), validators=[DataRequired()])
    submit = SubmitField(('提交'))


class EditProfileForm(Form):
    """
    表单 - 编辑资料
    """
    name = StringField(label=('名字:'), validators=[length(0, 64)])
    about_me = StringField(label=('关于我:'),
                           validators=[DataRequired(),
                                       length(0, 64)])
    submit = SubmitField(('提交'))


class EditProfileAdminForm(Form):
    """
    表单 - 编辑资料
    """
    email = StringField('Email',
                        validators=[DataRequired(),
                                    length(1, 64),
                                    Email()])
    name = StringField('name',
                       validators=[
                           DataRequired(),
                           length(1, 64),
                           Regexp(
                               '^[A-Za-z][A-Za-z0-9_.]*$', 0,
                               'Usernames must have only letters, '
                               'numbers, dots or underscores')
                       ])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        """
        校验邮箱
        """
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        """
        校验用户名
        """
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
