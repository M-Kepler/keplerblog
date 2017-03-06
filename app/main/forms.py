#coding:utf-8

#  from flask_wtf import Form
from flask_wtf import FlaskForm as Form

from ..models import Category, Role
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import StringField, SelectField, BooleanField, TextAreaField, SubmitField, validators, ValidationError
from wtforms.validators import DataRequired, length, Regexp, EqualTo, Email
from flask_pagedown.fields import PageDownField

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])

class PostForm(Form):
    title = StringField(label=('标题'), validators=[DataRequired()])
    #  category = SelectField(label=('文章分类:'), coerce=int)
    category = StringField("分类", validators=[DataRequired()])
    body = PageDownField(label=('正文'), validators=[DataRequired()])
    private = BooleanField("私人")
    submit = SubmitField(('提交'))

    def __init__(self,  *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices=[(category.id, category.name)
                for category in Category.query.order_by(Category.name).all()]



class AddCategoryForm(Form):
    categoryname = StringField('新分类', validators=[
        DataRequired(), length(1, 64)])
    submit=SubmitField('添加')
    def validate_username(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('分类已存在')


class CommentForm(Form):
    body = PageDownField(label=('Comment'), validators=[DataRequired()])
    submit = SubmitField(('提交'))

class EditProfileForm(Form):
    name = StringField(label=('名字:'), validators=[length(0,64)])
    about_me = StringField(label=('关于我:'), validators=[DataRequired(), length(0,64)])
    submit = SubmitField(('提交'))


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[DataRequired(), length(1, 64),
                                             Email()])
    name = StringField('name', validators=[
        DataRequired(), length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
