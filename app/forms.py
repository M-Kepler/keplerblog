# coding:utf-8
from flask.ext.wtf import Form

from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, length, Regexp, EqualTo, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectField
#  from flask.ext.pagedown.fields import PageDownField


class LoginForm(Form):
    #  DataRequired()为校验器,这样就不需要自己写代码进行校验了,也可以自己定义
    #  email = StringField(label='e-mail', validators = [DataRequired(), Email()])
    username = StringField(label='username', validators = [DataRequired()])
    password = PasswordField(label='password', validators = [DataRequired()])
    submit = SubmitField('Submit')

'''
class RegForm(Form):
    username = StringField(label='用户名:', validators = [Required(), length(6,18),
        Regexp('^[A-Za-z][A-Za-z0-9_.]$', 0,
            "用户名只允许字母", "用户名不允许特殊符号")])
    email = StringField(label='E-Mail', validators = [DataRequired(), Email()])
    password = PasswordField(label='密码:', validators = [DataRequired()])
    password1 = PasswordField(label='重复密码:', validators = [DataRequired(), EqualTo('password','密码不一致')])
    real_name = StringField("昵称", validators = [DataRequired()])
    submit = SubmitField("submit")

class PostArticleForm(Form):
    title = StringField("标题", validators = [Required(), length(6, 64)])
    body = TextAreaField("内容")
    category_id = QuerySelectField("分类", query_factory = lambda:Category.query.all(),
            get_pk = lambda a:str(a.id), get_label = lambda a:a.name)
    submit = StringField("发布")


class PostForm(Form):
    title = StringField(label='标题', validators=[DataRequired()])
    body = PageDownField(label=u'正文', validators=[DataRequired()])
    summit = SubmitField(u'发表')


class CommentForm(Form):
    body = PageDownField(label=u'评论', validators=[DataRequired()])
    summit = SubmitField(u'发表')
'''

