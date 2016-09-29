
from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,EqualTo,Email
#  from flask.ext.pagedown.fields import PageDownField


class LoginForm(Form):
    #  DataRequired()为校验器,这样就不需要自己写代码进行校验了,也可以自己定义
    username = StringField(label='username', validators = [DataRequired()])
    email = StringField(label='e-mail', validators = [DataRequired(), Email()])
    password = PasswordField(label='password', validators = [DataRequired()])
    submit = SubmitField('Submit')


class RegForm(Form):
    username = StringField(label='username', validators = [DataRequired()])
    email = StringField(label='E-Mail', validators = [DataRequired(), Email()])
    password = PasswordField(label='password', validators = [DataRequired()])
    password1 = PasswordField(label='password', validators = [DataRequired(), EqualTo('password','password not match')])
    submit = SubmitField("submit")



'''
class PostForm(Form):
    title = StringField(label='标题', validators=[DataRequired()])
    body = PageDownField(label=u'正文', validators=[DataRequired()])
    summit = SubmitField(u'发表')


class CommentForm(Form):
    body = PageDownField(label=u'评论', validators=[DataRequired()])
    summit = SubmitField(u'发表')
'''

