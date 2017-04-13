# coding :utf-8
from flask import flash, session, request, render_template, url_for, redirect, abort, current_app,g
from os import path
from . import main
from .. import db
from ..models import User, Role, Post, Comment, Category
from flask_login import login_required, current_user
from .forms import CommentForm, PostForm, EditProfileForm, EditProfileAdminForm, SearchForm
from ..config import DevelopmentConfig as config
from sqlalchemy import extract, func
from datetime import datetime

basepath = path.abspath(path.dirname(__file__))

@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    posts = Post.query.all()
    page_index = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(
            Post.create_time.desc()).paginate(
                    page_index, per_page = config.PER_POSTS_PER_PAGE,
                    error_out=False)
    posts=pagination.items

    categorys = Category.query.order_by(Category.id)[::-1] # 所有标签返回的是一个元组
    # 如果分类下的文章数为0, 就删掉这个分类
    for c in categorys:
        p = c.posts.all()
        if len(p) == 0: # 该分类下的文章数为0
            db.session.delete(c)

    #TODO 每个分类下的文章总数, 好像有必要分开分类和标签了
    return render_template('index.html', title = 'M-Kepler', posts = posts,
            categorys = categorys, pagination = pagination, current_time = datetime.utcnow())


    #  @app.route('/user/<int: user_id>')
#  @app.route('/user/<regex("[a-z]+"):name>')
@main.route('/user/<name>')
def user(name):
    user = User.query.filter_by(name=name).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/posts/<int:id>', methods = ['GET','POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if post.private and not current_user.is_administrator():
        flash("Sorry This is Personal Article.")
        return page_not_found(Exception("Not allowed to read"))
    post.read_count += 1

    #  保存评论
    if form.validate_on_submit():
        if current_user.is_anonymous:
            flash("PLEASE SIGNIN BEFORE COMMENT.")
            return redirect(url_for('auth.signin'))
        else:
            comment = Comment( author_id = current_user.id, body = form.body.data, post = post)
            db.session.add(comment)
            flash('COMMENT PUBLISHED.')
            return redirect(url_for('.post', id=post.id, page=-1))
    comment_count = len(post.comments)

#  TODO
    #  page_index = request.args.get('page', 1, type=int)
    #  if page_index == -1:
        #  page_index = (comment_count-1)//config.PER_POSTS_PER_PAGE + 1

    #  pagination = post.comments.query.order_by(Comment.create_time.desc()).paginate(
            #  page_index, per_page = config.PER_POSTS_PER_PAGE, error_out = False)
    #  comments= pagination.items
    #  return render_template('posts/detail.html', title='M-Kepler | ' + post.title, form=form, post=post, comments=comments, pagination = pagination, comment_count = comment_count)


    form.body.data = ''
    categorys = Category.query.order_by(Category.id)[::-1] # 所有标签返回的是一个元组
    return render_template('posts/detail.html', title='M-Kepler | ' + post.title, form=form, post=post,
            categorys=categorys, comment_count = comment_count)



#  定义一个装饰器, 修饰只有管理员才能访问的路由
from functools import wraps
def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_user.is_administrator():
            return f(*args, **kwargs)
        else:
            abort(403)
    return decorator


#  把输入框的字串用, 分开, 然后转化为category对象，现在已经没用了
def str_to_obj(new_category):
    c =[]
    for category in new_category:
        category_obj=Category.query.filter_by(name=new_category).first()
        if category_obj is None:
            category_obj = Category(name=new_category)
            c.append(category_obj)
    return category_obj

@main.route('/edit', methods = ['GET', 'POST'])
@main.route('/edit/<int:id>', methods = ['GET','POST'])
@login_required
@admin_required
def edit(id=0):
    form = PostForm()
    if id == 0: # 新增, current_user当前登录用户
        post = Post(author_id = current_user.id)
    else:
        post = Post.query.get_or_404(id)


    if form.validate_on_submit():
        categoryemp = []
        category_list = form.category.data.split(',')
        # 如果已经有这个分类就不用创建
        for t in category_list:
            tag = Category.query.filter_by(name=t).first()
            if tag is None:
                tag = Category()
                tag.name = t
                #  tag.save()
            categoryemp.append(tag)

        post.categorys = categoryemp
        post.title = form.title.data
        post.body = form.body.data

        post.private = form.private.data
        post.read_count = 0

        db.session.add(post)
        db.session.commit()
        db.session.rollback()
        return redirect(url_for('.post', id=post.id))

    form.title.data = post.title
    #  form.body.data = post.body
    body_value= post.body

    #  form.category.data = [i.name for i in post.categorys]
    #  value = [i.name for i in post.categorys]
    # TODO ☆ 为了把值传到input标签,我也没其他方法了, 然后将category的list元素用‘,’分割组成str传给input
    value = ",".join([i.name for i in post.categorys])

    mode='编辑' if id>0 else '添加'
    return render_template('posts/edit.html', title ='%s - %s' % (mode, post.title), form=form,
            post=post, value=value, body_value = body_value)


@main.route('/posts/delete/<int:id>', methods = ['GET','POST'])
@login_required
def deletepost(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    for comment in post.comments:
        db.session.delete(comment)
#   如果分类下没有文章了就删掉这个分类
    for category in post.categorys.all():
        if category.posts.all() is None:
            db.session.delete(category)
    flash('POST DELETED')
    return redirect(url_for('.index'))


# FIXME 评论删除后显示的是当前这篇文章啊
@main.route('/comment_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def comment_delete(id):
    comment = Comment.query.get_or_404(id)
    post_id = comment.post_id
    db.session.delete(comment)
    flash('COMMENT DELETED')
    return redirect(url_for('.post', id=post_id))


@main.route('/category/<name>', methods=['GET', 'POST'])
def category(name):
    #  点击index的标签后跳到这里,顺便把标签名传了过来,
    #  index视图那里也不需要进行查询,因为做了外键,直接可以有posts知道category
    categorys = Category.query.order_by(Category.id)[::-1] # 右侧需要显示的所有标签
    category = Category.query.filter_by(name = name).first() # name对应的标签对象
    page_index = request.args.get('page', 1, type=int)

    #  pagination = Post.query.filter(Post.categorys == category).order_by(
    pagination = category.posts.order_by(Post.create_time.desc()).paginate(
                    page_index, per_page = config.PER_POSTS_PER_PAGE,
                    error_out=False)
    posts=pagination.items
    return render_template("category.html",title='M-Kepler|分类|' + name, name=name, posts=posts, categorys=categorys, pagination=pagination)


# 分类管理
@main.route('/category_manager', methods=['GET', 'POST'])
def category_manager():
    return "category_manager test"

@main.route('/category/delete<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def category_delete(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    '''
    分来下的文章也删除吗?还是自动划分到other分类下?
    for comment in post.comments:
        db.session.delete(comment)
    '''
    flash('该分类已删除')
    return redirect(url_for('.index'))


@main.route('/category/edit<int:id>', methods=['GET', 'POST'])
@admin_required
@login_required
def category_edit(id=0):
    pass


@main.route('/archive')
def archive():
    #  返回一个元素是tuple的列表[(10, 32), (11, 23), (12, 1)] #  tuple第一个关键码标识月份，第二个标识数量 #  我试了试提取year, 会出错
    archives = db.session.query(extract('month', Post.create_time).label('month'),
            func.count('*').label('count')).group_by('month').all()

    posts=[]
    for archive in archives:
        posts.append((archive[0], db.session.query(Post).filter(extract('month', Post.create_time)==archive[0]).all()))

    return render_template('archive.html',title='M-Kepler | ARCHIVE', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html', title='M-Kepler | ABOUT')

@main.route('/search', methods=['GET', 'POST'])
def search():
    return 'test'


@main.before_app_request
def before_request():
    #  if current_user.is_authenticated: #  全文搜索,让这个搜索框
    g.search_form = SearchForm()


@main.route('/edit-profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.name.data:
            current_user.name = form.name.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('你的资料已更新.')
        return redirect(url_for('.user', name=current_user.name))
    form.name.date = current_user.name
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form = form)


@main.route('/edit-profile/<int:id>', methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('You Profile has been updated.')
        return redirect(url_for('.user', name=user.name))
    form.email.data = user.email
    form.name.data = user.name
    form.confirmed.data = user.confirmed
    form.role.data = user.role.name
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form = form, user=user)


#  TODO
@main.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', code=404, e=e), 404
@main.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', code=500, e=e), 500

'''
#  上传文件
@main.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method=='POST':
        f = request.files['file']
        basepath = path.abspath(path.dirname(__file__))
        upload_path = path.join(basepath,'static/uploads')
        f.save(upload_path, secure_filename(f.filename))
        return redirect(url_for('main.upload'))
    return render_template('upload.html')

@main.route('/projects/')
def projects():
    return render_template('projects.html')



#  定义自己的jinja2过滤器
@app.template_filter('reverse')
def reverse_filter(s):
    return s[::-1]

@app.template_filter('md')
def markdown_to_html(txt):
    from markdown import markdown
    return markdown(txt)

#  -------------
#  通过上下文处理器把方法注册进去,这样所有模板都可以使用这个方法/变量
#  所以就可以将文件读取到变量然后传递到jinja供模板使用,
#  读取md文件并显示到模板中
def read_md(filename):
    with open(filename) as md_file:
        content = reduce(lambda x, y: x + y, md_file.readlines()) #  读取文件,注意reduce要从functools导入
    return content

#  注册方法到程序上下文
@app.context_processor
def inject_methods():
    return dict(read_md=read_md)

@app.template_test('current_link')
def is_current_link(link):
    return link[0] is request.url

def qsbk():
    lines = f.readlines()
    return render_template('qsbk.html',lines=lines)

'''
