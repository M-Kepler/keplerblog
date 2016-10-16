from flask import flash, session, request, render_template, url_for, redirect, abort, current_app
from .forms import LoginForm, RegForm
from ..models import User
from .. import db
from ..emails import send_email
from . import auth
from flask.ext.login import login_required, login_user, logout_user, current_user


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remeber_me.data)
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
                )
        user.password=form.password.data
        db.session.add(user)
        db.session.commit()
        #  生成验证token
        token = user.generate_confirmation_token()
        #  发送确认邮件, 邮件模板放在/templates/auth/email
        send_email(
                user.email, 'ConfirmYouAccount',
                '/auth/email/confirm', user=user, token=token
                )
        flash(' A Confirmation email has been sent to you by email.')
        return redirect(url_for('auth.signin'))
    return render_template('signup.html', title='注册', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed: # 已经确认过了
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


#  --- 可以过滤显示给未确认用户看的 ---
#  请求钩子
@auth.before_app_request
def before_request():
    # User模型继承了UserMinxin的好处,可以调用这些函数看是否已经确认等等
    if current_user.is_authenticated()\
            and not current_user.confirmed\
            and request.endpoint[:5] != 'auth.'\
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.isannoymouse() or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

#  --- 可以过滤显示给未确认用户看的 ---

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
            'auth/email/confirm', user = current_user, token=token)
    flash('A new confirmation email has been send to your email.')
    return redirect(url_for('main.index'))




@auth.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('main.index'))

