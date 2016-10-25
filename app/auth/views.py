# coding:utf-8
from flask import flash, session, request, render_template, url_for, redirect, abort, current_app
from .forms import LoginForm, RegForm
from ..models import User
from .. import db
from ..emails import send_email
from . import auth
from flask_login import login_required, login_user, logout_user, current_user


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember = form.remember_me.data) # 记住我, 一个cookie会存储在计算机中
            #  login_user(user) # 记住我, 一个cookie会存储在计算机中
            return redirect(url_for('main.user', name = current_user.name))
        else:
            flash("wrong username or userpassword")
            return redirect(url_for('auth.signin'))
    return render_template('signin.html', title='登录', form=form)


@auth.route('/signup', methods=['GET','POST'])
def signup():
    form = RegForm()
    if form.validate_on_submit():
        user=User(
                name = form.username.data,
                email = form.email.data,
                about_me = form.about_me.data
                )
        # 传入密码到models里,然后计算passwd_hash
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token() #  生成验证token
        #  发送确认邮件, 邮件模板放在/templates/auth/email
        send_email(
                user.email, 'ConfirmYouAccount',
                '/auth/email/confirm', user=user, token=token
                )
        flash(' A Confirmation email has been sent to you by email.')
        return redirect(url_for('auth.signin'))
    return render_template('signup.html', title='注册', form=form)


#  发给用户的连接就是这个路由,后面的token用来校验,
#  用户点击确认链接就是访问这个路由,顺带将token传到Models.Users里的confirm函数
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed: # User模型的confirmed字段,已经确认过了
        return redirect(url_for('main.index'))
    if current_user.confirm(token): # 用户点击链接访问了这个视图
        flash('You have confirmed your account. Thanks!')
    else: # token 过期了
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


#  --- 在用户确认邮箱之前只显示某些页面 ---
#  请求钩子,如果已经登录但是还没有确认,或请求auth蓝图以外的视图,都会跳到unconfirmed
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
            'auth/email/confirm', user = current_user, token=token)
    flash('A new confirmation email has been send to you by email.')
    return redirect(url_for('main.index'))



@auth.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('main.index'))

