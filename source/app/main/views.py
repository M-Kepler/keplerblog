# coding :utf-8

"""
视图

view.py 中导入对应的蓝图，并将视图函数注册到蓝图中

"""

from datetime import datetime
from functools import wraps

from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required
from sqlalchemy import extract, func

from ..config import DevelopmentConfig as config
from ..models.category import Category
from ..models.comment import Comment
from ..models.post import Post
from ..models.role import Role
from ..models.user import User
from ..plugins import db
from .forms import CommentForm, EditProfileAdminForm, EditProfileForm, PostForm

# main 表示蓝图的名称，一般和 url_prefx 保持一致
main = Blueprint("main", __name__, url_prefix='/')


@main.route("/", methods=["GET", "POST"])
@main.route("/index", methods=["GET", "POST"])
def home():
    """
    首页视图
    """

    posts = Post.query.all()
    page_index = request.args.get("page", 1, type=int)
    pagination = Post.query.order_by(Post.create_time.desc()).paginate(
        page=page_index, per_page=config.PER_POSTS_PER_PAGE, error_out=False)
    posts = pagination.items

    categorys = Category.query.order_by(Category.id)[::-1]  # 所有标签返回的是一个元组
    # 如果分类下的文章数为0, 就删掉这个分类
    for item in categorys:
        if item.posts.count() == 0:
            db.session.delete(item)

    return render_template("index.html",
                           title="M-Kepler",
                           posts=posts,
                           categorys=categorys,
                           pagination=pagination,
                           current_time=datetime.utcnow())


@main.route("/user/<name>")
def user_view(name):
    """
    用户页面视图
    """
    user_info = User.query.filter_by(name=name).first()
    if not user_info:
        abort(404)
    return render_template("users/user.html", user=user_info)


@main.route("/posts/<int:post_id>",
            endpoint="post_view",
            methods=["GET", "POST"])
def post_func(post_id):
    """
    文章页面视图
    endpoint 就像是替身，指定后，URL 和函数名随便变动，其他引用的地方都不会有影响
    """
    post_info = Post.query.get_or_404(post_id)
    form = CommentForm()

    # 不允许访问私密文章
    if post_info.private and not current_user.is_administrator():
        flash("Sorry This is a Personal Article.")
        return page_not_found(Exception("Not allowed to read"))

    # 记录访问数
    post_info.read_count += 1

    # 保存评论
    if form.validate_on_submit():
        if current_user.is_anonymous:
            flash("PLEASE SIGNIN BEFORE COMMENT.")
            return redirect(url_for("auth.signin"))
        else:
            comment = Comment(author_id=current_user.id,
                              body=form.body.data,
                              post=post_info)
            db.session.add(comment)
            flash("COMMENT PUBLISHED.")
            return redirect(
                url_for(".post_view", post_id=post_info.id, page=-1))
    comment_count = len(post_info.comments)

    # TODO 评论分页
    """
    page_index = request.args.get("page", 1, type=int)
    if page_index == -1:
        page_index = (comment_count-1)//config.PER_POSTS_PER_PAGE + 1

    pagination = post.comments.query.order_by(
        Comment.create_time.desc()).paginate(page_index,
            per_page = config.PER_POSTS_PER_PAGE, error_out = False)
    comments= pagination.items
    return render_template(
        "posts/detail.html",
        title="M-Kepler | " + post.title,
        form=form,
        post=post,
        comments=comments,
        pagination=pagination,
        comment_count=comment_count)
    """

    form.body.data = ""
    categorys = Category.query.order_by(Category.id)[::-1]  # 所有标签返回的是一个元组
    return render_template("posts/detail.html",
                           title="M-Kepler | " + post_info.title,
                           form=form,
                           post=post_info,
                           categorys=categorys,
                           comment_count=comment_count)


def admin_required(f):
    """
    超级管理员装饰器
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_user.is_administrator():
            return f(*args, **kwargs)
        else:
            abort(403)

    return decorator


def str_to_obj(new_category):
    """
    把输入框的字串用, 分开, 然后转化为category对象，现在已经没用了
    """
    c = []
    for item in new_category:
        category_obj = Category.query.filter_by(name=item).first()
        if category_obj is None:
            category_obj = Category(name=item)
            c.append(category_obj)
    return category_obj


@main.route("/edit_post", methods=["GET", "POST"])
@main.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_post_view(post_id=0):
    """
    视图 - 编辑文章
    """
    form = PostForm()
    # 新增, current_user当前登录用户
    if post_id == 0:
        post = Post(author_id=current_user.id)
    else:
        post = Post.query.get_or_404(post_id)

    if form.validate_on_submit():
        # 表单提交时，触发校验
        categoryemp = []
        category_list = form.category.data.split(",")
        # 如果已经有这个分类就不用创建
        for t in category_list:
            tag = Category.query.filter_by(name=t).first()
            if tag is None:
                tag = Category()
                tag.name = t
                # tag.save()
            categoryemp.append(tag)

        post.categorys = categoryemp
        post.title = form.title.data
        post.body = form.body.data

        post.private = form.private.data
        post.read_count = 0

        db.session.add(post)
        db.session.commit()
        db.session.rollback()
        return redirect(url_for(".post_view", post_id=post.id))

    form.title.data = post.title
    body_value = post.body

    # TODO 为了把值传到input标签,我也没其他方法了, 然后将category的list元素用‘,’分割组成str传给input
    value = ",".join([i.name for i in post.categorys])

    mode = "编辑" if post_id > 0 else "添加"
    return render_template("posts/edit.html",
                           title=f"{mode} - {post.title}",
                           form=form,
                           post=post,
                           value=value,
                           body_value=body_value)


@main.route("/posts/delete/<int:post_id>", methods=["GET", "POST"])
@login_required
def delete_post_view(post_id):
    """
    视图 - 删除文章
    """
    post_info = Post.query.get_or_404(post_id)
    db.session.delete(post_info)
    for comment in post_info.comments:
        db.session.delete(comment)

    # 如果分类下没有文章了就删掉这个分类
    for category in post_info.categorys.all():
        if category.posts.all() is None:
            db.session.delete(category)
    flash("POST DELETED")
    return redirect(url_for(".home"))


@main.route("/comment_delete/<int:comment_id>", methods=["GET", "POST"])
@login_required
def delete_comment_view(comment_id):
    """
    删除文章评论
    """
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post_id
    db.session.delete(comment)
    flash("COMMENT DELETED")
    return redirect(url_for(".post_view", post_id=post_id))


@main.route("/category/<name>", methods=["GET", "POST"])
def category_view(name):
    """
    获取分类
    """
    # 点击 index 的标签后跳到这里,顺便把标签名传了过来,
    # index 视图那里也不需要进行查询,因为做了外键，直接可以由 posts 知道 category
    categorys = Category.query.order_by(Category.id)[::-1]  # 右侧需要显示的所有标签
    category = Category.query.filter_by(name=name).first()  # name对应的标签对象
    page_index = request.args.get("page", 1, type=int)

    pagination = category.posts.order_by(Post.create_time.desc()).paginate(
        page=page_index, per_page=config.PER_POSTS_PER_PAGE, error_out=False)
    posts = pagination.items
    return render_template("posts/category.html",
                           title="M-Kepler|Category|" + name,
                           name=name,
                           posts=posts,
                           categorys=categorys,
                           pagination=pagination)


@main.route("/category_manager", methods=["GET", "POST"])
def category_manager_view():
    """
    TODO 分类管理
    """

    return "category_manager test"


@main.route("/category/delete<int:category_id>", methods=["GET", "POST"])
@admin_required
@login_required
def delete_category_view(category_id):
    """
    删除分类
    """
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    """
    XXX 分来下的文章也删除吗?还是自动划分到other分类下?
    for comment in post.comments:
        db.session.delete(comment)
    """
    flash("该分类已删除")
    return redirect(url_for(".home"))


@main.route("/category/edit<int:category_id>", methods=["GET", "POST"])
@admin_required
@login_required
def edit_category_view(category_id=0):
    """
    TODO 编辑分类
    """
    pass


@main.route("/archive")
def archive_view():
    """
    归档
    """
    # 返回一个元素是tuple的列表[(10, 32), (11, 23), (12, 1)]
    # tuple 第一个关键码表示月份，第二个表示数量
    # 我试了试提取 year, 会出错
    archives = db.session.query(
        extract("month", Post.create_time).label("month"),
        func.count("*").label("count")).group_by("month").all()

    posts = []
    # TODO 没有按照月份进行 group
    for archive in archives:
        posts.append((archive[0], db.session.query(Post).filter(
            extract("month", Post.create_time) == archive[0]).all()))

    return render_template("archive.html",
                           title="M-Kepler | ARCHIVE",
                           posts=posts)


@main.route("/about")
def about_view():
    """
    关于我
    """
    return render_template("about.html", title="M-Kepler | ABOUT")


@main.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile_view():
    """
    资料编辑
    """
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.name.data:
            current_user.name = form.name.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash("你的资料已更新.")
        return redirect(url_for(".user_view", name=current_user.name))
    form.name.date = current_user.name
    form.about_me.data = current_user.about_me
    return render_template("users/edit_profile.html", form=form)


@main.route("/edit-profile/<int:user_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_profile_admin_view(user_id):
    """
    管理员编辑资料
    """
    user = User.query.get_or_404(user_id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.about_me = form.about_me.data
        db.session.add(user)
        flash("You Profile has been updated.")
        return redirect(url_for(".user_view", name=user.name))
    form.email.data = user.email
    form.name.data = user.name
    form.confirmed.data = user.confirmed
    form.role.data = user.role.name
    form.about_me.data = user.about_me
    return render_template("users/edit_profile.html", form=form, user=user)


@main.errorhandler(404)
def page_not_found(e):
    """
    TODO 404
    """
    return render_template("error.html", code=404, e=e), 404


@main.errorhandler(500)
def internal_server_error(e):
    """
    TODO 500
    """
    return render_template("error.html", code=500, e=e), 500


"""
# 上传文件

from os import path
@main.route("/upload", methods = ["GET", "POST"])
def upload():
    if request.method=="POST":
        f = request.files["file"]
        basepath = path.abspath(path.dirname(__file__))
        upload_path = path.join(basepath,"static/uploads")
        f.save(upload_path, secure_filename(f.filename))
        return redirect(url_for("main.upload"))
    return render_template("upload.html")

@main.route("/projects/")
def projects():
    return render_template("projects.html")



# 定义自己的jinja2过滤器
@app.template_filter("reverse")
def reverse_filter(s):
    return s[::-1]

@app.template_filter("md")
def markdown_to_html(txt):
    from markdown import markdown
    return markdown(txt)

# -------------
# 通过上下文处理器把方法注册进去,这样所有模板都可以使用这个方法/变量
# 所以就可以将文件读取到变量然后传递到jinja供模板使用,
# 读取md文件并显示到模板中
def read_md(filename):
    with open(filename) as md_file:
        # 读取文件,注意reduce要从functools导入
        content = reduce(lambda x, y: x + y, md_file.readlines())
    return content

# 注册方法到程序上下文
@app.context_processor
def inject_methods():
    return dict(read_md=read_md)

@app.template_test("current_link")
def is_current_link(link):
    return link[0] is request.url

def qsbk():
    lines = f.readlines()
    return render_template("qsbk.html",lines=lines)

"""
