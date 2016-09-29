#_*_coding:utf-8_*_

from flask import Flask,flash, session, request, render_template, url_for, redirect, abort, current_app
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename

from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.nav import Nav
from flask_nav.elements import *
from flask.ext.moment import Moment

from os import path
from datetime import datetime
from functools import reduce


f = open("qsbk.txt",'r')

#  为路由规则增加正则转换器
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex=items[0]


#  初始化
app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter

#  防止跨站点攻击,所以需要识别该post请求是我自己的form返回的请求
app.config.from_pyfile('config')
#  app.config['SECRET_KEY']='this is a secret key'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment=Moment(app)

#  应用这个导航栏插件就不需要自己写导航栏了,
#  可以用操作对象的形式来设置导航栏
#  注册到导航栏对象top
nav = Nav()
nav.register_element('top', Navbar('M_Kepler',
    View('Home', 'home'),
    View('Signin', 'signin'),
    View('Login', 'login'),
    View('Qsbk', 'qsbk'),
    View('Upload', 'upload'),
    View('Project', 'projects'),
    View('About', 'about'),
    ))
nav.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='M_Kepler',artical='<h1>Hello \t\n world')
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
    #  这里将form写在了form.py,将form对象实例化传递到模板login.html
    from forms import LoginForm
    form = LoginForm()
    #  获取表单数据并进行验证
    if form.validate_on_submit():
        session['username'] = form.username.data
        session['password'] = form.password.data
        if session['username']=='admin' and session['password']=='passwd':
            flash('welcome login') #  显示flash信息
    return render_template('login.html', title='登录', form=form)
    #  name = session['username']
    #  return redirect(url_for('user'),name=name)


@app.route('/qsbk')
def qsbk():
    lines = f.readlines()
    return render_template('qsbk.html',lines=lines)


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


@app.route('/projects/')
def projects():
    return 'This is the project page'


@app.route('/about')
def about():
    return render_template('about.html')

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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)


@manager.command
def test():
    pass


@manager.command
def deplay():
    pass






if __name__ == '__main__':
    # 程序上下文
    app_ctx=app.app_context()
    app_ctx.push()
    print('current_app name :%s' % current_app.name)
    #  manager.run()
    app.run(debug=True)

