#coding:utf-8

from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, SubmitField, validators, ValidationError
from wtforms.validators import DataRequired, length, Regexp, EqualTo, Email
from flask_pagedown.fields import PageDownField


class PostForm(Form):
    title = StringField(label=('标题:'), validators=[DataRequired()])
    body = PageDownField(label=('正文:'), validators=[DataRequired()])
    submit = SubmitField(('提交'))


class CommentForm(Form):
    body = PageDownField(label=('Comment'), validators=[DataRequired()])
    submit = SubmitField(('提交'))

'''
class EditProfileForm(Form):
    name = StringField(label=('名字:'), validators=[DataRequired(), length(0,64)])
    about_me = StringField(label=('关于我:'), validators=[DataRequired(), length(0,64)])
    submit = SubmitField(('提交'))
    '''
