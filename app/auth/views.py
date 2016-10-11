
from flask import flash, session, request, render_template, url_for, redirect, abort, current_app
#  from forms import LoginForm, RegForm
from .forms import LoginForm, RegForm
from ..models import User
from . import auth


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
                user_name=form.username.data,
                user_passwd=form.password.data).all()
        session['username'] = form.username.data
        if user:
            return redirect(url_for('main.user',name = session['username']))
        else:
            flash("wrong username or userpassword")
    return render_template('signin.html', title='登录', form=form)


@auth.route('/signup', methods=['GET','POST'])
def signup():
    form = RegForm()
    if form.validate_on_submit():
        user=User(
                user_name = form.username.data,
                #  user_email = form.email.data,
                user_passwd = form.password.data
                )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.signin'))
    return render_template('signup.html', title='注册', form=form)

@auth.route('/signout')
def signout():
    pass

