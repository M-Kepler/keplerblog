#coding:utf-8

from flask_wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, SubmitField, validators, ValidationError
from wtforms.validators import DataRequired, length, Regexp, EqualTo, Email
from flask_pagedown.fields import PageDownField


class PostForm(Form):
    title = StringField(label=('标题:'), validators=[DataRequired()])
    body = PageDownField(label=('正文:'), validators=[DataRequired()])
    submit = SubmitField(('Submit'))


class CommentForm(Form):
    body = PageDownField(label=('Comment'), validators=[DataRequired()])
    submit = SubmitField(('Submit'))

