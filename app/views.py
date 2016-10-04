# coding :utf-8

from flask import flash, session, request, render_template, url_for, redirect, abort, current_app
from os import path


basepath = path.abspath(path.dirname(__file__))
#  basepath = path.abspath('.')
filename = path.join(basepath,'vim_end.md')

def init_views(app):
    @app.route('/', methods=['GET', 'POST'])
    def home():
        return render_template('home.html', title='M_Kepler',artical='<h1>Hello \t\n world')
        #  return render_template('home.html', title='M_Kepler',artical = '<h1>Hello \t\n world</h1>', body = '# test ')
        #  return render_template('home.html',
                #  current_time=datetime.utcnow(),
                #  title="<h1>Hello\t\n world</h1>",
                #  body="### Hello world again ###"
                #  )

    #  @app.route('/user/<int: user_id>')
    #  @app.route('/user/<name>')
    @app.route('/user/<regex("[a-z]+"):name>')
    def user(name):
        return render_template('user.html', name=name)


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        from .forms import LoginForm
        #  这里将form写在了form.py,将form对象实例化传递到模板login.html
        form = LoginForm()
        #  获取表单数据并进行验证
        if form.validate_on_submit():
            #  session['username'] = form.username.data
            #  session['password'] = form.password.data
            #  if session['username']=='admin' and session['password']=='passwd':
                #  flash('welcome login') #  显示flash信息
                    #  return redirect(url_for('user',name = session['username']))
            username = form.username.data
            password = form.password.data
            if username =='admin' and password =='passwd':
                return redirect(url_for('user',name = username))
        return render_template('login.html', title='登录', form=form)
        #  name = session['username']
        #  return redirect(url_for('user'),name=name)


    #  @app.route('/qsbk')
    #  def qsbk():
        #  lines = f.readlines()
        #  return render_template('qsbk.html',lines=lines)


    @app.route('/signin', methods=['GET','POST'])
    def signin():
        if request.method == 'GET':
            return render_template('form.html')
        else:
            #  从表单获取数据
            username = request.form['username']
            password = request.form['password']
            if username=='admin' and password=='password':
                return redirect(url_for('user',name=username))
                   #  return render_template('user.html', name=username)
            return render_template('form.html', message='Bad username or password',
                    username=username)


    #  上传文件
    @app.route('/upload', methods = ['GET', 'POST'])
    def upload():
        if request.method=='POST':
            f = request.files['file']
            basepath = path.abspath(path.dirname(__file__))
            upload_path = path.join(basepath,'static/uploads')
            f.save(upload_path, secure_filename(f.filename))
            return redirect(url_for('upload'))
        return render_template('upload.html')


    @app.route('/signout')
    def signout():
        return 'signout'


    @app.route('/archive')
    def archive():
        return render_template('archive.html')


    @app.route('/projects/')
    def projects():
        return render_template('projects.html')


    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404


    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    #  定义自己的jinja2过滤器
    @app.template_filter('md')
    def markdown_to_html(txt):
        from markdown import markdown
        return markdown(txt)

    #  通过上下文处理器把方法注册进去,这样所有模板都可以使用这个方法/变量
    #  所以就可以将文件读取到变量然后传递到jinja供模板使用,
    #  读取md文件并显示到模板中
    def read_md(filename):
        with open(filename) as md_file:
            #  读取文件,注意reduce要从functools导入
            content = reduce(lambda x, y: x + y, md_file.readlines())
        return content
        #  return content.decode('utf-8')

    #  注册方法到程序上下文
    @app.context_processor
    def inject_methods():
        return dict(read_md=read_md)

    @app.template_test('current_link')
    def is_current_link(link):
        return link[0] is request.url



