#coding:utf-8

from flask_wtf import Form
from ..models import Category
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import StringField, SelectField, BooleanField, TextAreaField, SubmitField, validators, ValidationError
from wtforms.validators import DataRequired, length, Regexp, EqualTo, Email
from flask_pagedown.fields import PageDownField

class PostForm(Form):
    title = StringField(label=('标题:'), validators=[DataRequired()])
    #  category = QuerySelectField('分类:', query_factory=get_category_factory, get_label='name')
    category = SelectField(label=('文章分类:'), coerce=int)
    body = PageDownField(label=('正文:'), validators=[DataRequired()])
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
    name = StringField(label=('名字:'), validators=[DataRequired(), length(0,64)])
    about_me = StringField(label=('关于我:'), validators=[DataRequired(), length(0,64)])
    submit = SubmitField(('提交'))
