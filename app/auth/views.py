from flask import flash, session, request, render_template, url_for, redirect, abort, current_app
from .forms import LoginForm, RegForm
from ..models import User
from .. import db
from . import auth
from flask.ext.login import login_user, logout_user, current_user


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

        '''
        user = User.query.filter_by(
                email=form.email.data,
                passwd=form.password.data).first()
        if user:
            login_user(user)
            return redirect(url_for('main.user', name = "admin"))
        else:
            flash("wrong username or userpassword")
            return redirect(url_for('auth.signin'))
        '''
    return render_template('signin.html', title='登录', form=form)


@auth.route('/signup', methods=['GET','POST'])
def signup():
    form = RegForm()
    if form.validate_email(form.email):
        flash('邮箱地址已注册')

    if form.validate_on_submit():
        user=User(
                name = form.username.data,
                email = form.email.data,
                )
        user.password=form.password.data

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.signin'))
    return render_template('signup.html', title='注册', form=form)


@auth.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('main.index'))

