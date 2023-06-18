# coding:utf-8

"""
auth 模块视图

"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ..emails import send_email
from ..models.user import User
from ..plugins import db
from .forms import LoginForm, RegForm, ResetPassword

auth = Blueprint("auth", __name__)


@auth.route("/signin", methods=["GET", "POST"])
def signin():
    """
    登录
    """
    form = LoginForm()
    if form.validate_on_submit():
        # 查看该邮箱是否已注册
        user = User.query.filter_by(
            email=form.email.data).first_or_404()
        if user is not None and user.verify_password(form.password.data):
            # 记住我, 一个cookie会存储在计算机中
            login_user(user,
                       remember=form.remember_me.data)
            return redirect(url_for("main.home"))
        else:
            flash("用户名或密码错误")
            return redirect(url_for("auth.signin"))
    return render_template("auth/signin.html", title="登录", form=form)


@ auth.route("/signup", methods=["GET", "POST"])
def signup():
    """
    用户注册
    """
    form = RegForm()
    if form.validate_on_submit():
        # 提交表单内容
        user = User(name=form.username.data,
                    email=form.email.data,
                    about_me=form.about_me.data)
        # 传入密码到models里,然后计算passwd_hash
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()  # 生成确认邮件的验证token
        send_email(user.email,
                   "ConfirmYouAccount",
                   "/auth/email/confirm",
                   user=user,
                   token=token)
        # flash(" A Confirmation email has been sent to you.")
        flash(" 已发送确认邮件.")
        return redirect(url_for("auth.signin"))
    return render_template("auth/signup.html", title="注册", form=form)


@ auth.route("/search", methods=["GET", "POST"])
def search():
    """
    搜索
    """
    return "test"


@ auth.route("/confirm/<token>")
@ login_required
def confirm(token):
    """
    发给用户的连接就是这个路由,后面的token用来校验,
    用户点击确认链接就是访问这个路由,顺带将token传到Models.Users里的confirm函数
    """
    if current_user.confirmed:  # User模型的confirmed字段,已经确认过了
        return redirect(url_for("main.home"))
    if current_user.confirm(token):  # 用户点击链接访问了这个视图
        flash("You have confirmed your account. Thanks!")
    else:  # token 过期了
        flash("The confirmation link is invalid or has expired.")
    return redirect(url_for("main.home"))


@ auth.before_app_request
def before_request():
    """
    --- 在用户确认邮箱之前只显示某些页面 ---
    请求钩子,如果已经登录但是还没有确认,或请求auth蓝图以外的视图,都会跳到unconfirmed # 每次请求之前运行
    """
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != "auth." \
                and request.endpoint != "static":
            return redirect(url_for("auth.unconfirmed"))


@ auth.route("/unconfirmed")
def unconfirmed():
    """
    邮箱未确认
    """
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("main.home"))
    return render_template("auth/unconfirmed.html")


@ auth.route("/confirm")
@ login_required
def resend_confirmation():
    """
    重发邮件
    """
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,
               "Confirm Your Account",
               "auth/email/confirm",
               user=current_user,
               token=token)
    flash("A new confirmation email has been send to you by email.")
    return redirect(url_for("main.home"))


@ auth.route("/signout")
def signout():
    """
    登出
    """
    logout_user()
    return redirect(url_for("main.home"))


@ auth.route("/resetpasswd", methods=["GET", "POST"])
def resetpasswd():
    """
    重置密码
    """
    form = ResetPassword()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            # 修改密码
            db.session.add(current_user)
            # 加入数据库的session，这里不需要.commit()，在配置文件中已经配置了自动保存
            flash("Your password has been updated.")
            return redirect(url_for("main.home"))
        else:
            flash("Invalid password.")
    return render_template("auth/reset_passwd.html", form=form)
