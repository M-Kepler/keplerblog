# coding:utf-8
from werkzeug.utils import secure_filename
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand, upgrade
from app import create_app, db
from app.models import User, Role, Category, Post, Comment
from livereload import Server
from werkzeug.security import generate_password_hash

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
#  数据库更新迁移,就好像git一样做版本控制的

#  也可以写带参数的脚本
@manager.command
def dev():
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url_delay=True)

#  进入shell调试的时候每次都要导入db,models太麻烦了,
#  所以配置一下shell命令的上下文,就可以在shell里用了,不用每次都导入
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post,Comment=Comment, Category=Category)

manager.add_command("shell", Shell(make_context=make_shell_context))




@manager.command
def test():
    pass



@manager.command
def save():
    # 使用orm框架保存
    user = User(1, "M01", "123456")
    db.session.add(user)
    db.session.commit()
    # 不使用orm框架:python manager.py save\ python manager.py query_all
    #  user = User(4, 'M04', '123456')

@manager.command
def query_all():
    #  users = User.query_all()
    users = User.query.all()
    for u in users:
        print(u)

#  生成测试数据
@manager.command
def fake():
    User.generate_fake()
    Category.generate_fake()
    Post.generate_fake()
    Comment.generate_fake()

@manager.command
def userfake():
    User.generate_fake()

@manager.command
def postfake():
    Post.generate_fake()

@manager.command
def commentfake():
    Comment.generate_fake()

@manager.command
def categoryfake():
    Category.generate_fake()

# 添加默认管理员
@ manager.option('-u',  '--name', dest='name')
@ manager.option('-e', '--email', dest='email')
@ manager.option('-p', '--password', dest='password')
def create_user(name, email, password):
    if name is None:
        name = input('Username(default admin):') or 'admin'
    if email is None:
        email = input('Email:')
    if password is None:
        password= input('Password:')
        #  password = getpassword('Password:')
    user = User()
    user.name = name
    #  这个hash我在models那边算了
    #  user.password = generate_password_hash(password)
    user.password = password

    user.email = email
    user.is_administrator = True
    user.confirmed = 1
    role = Role.query.filter_by(name='administrators').first()
    if role is None:
        role = Role()
        role.name = 'administrator'
    user.role = role
    db.session.add(user)
    db.session.commit()


#  部署还是能用的
@manager.command
def deploy():
    upgrade()
    Role.seed()
    Category.seed()


if __name__ == '__main__':
    manager.run()
    # 程序上下文
    #  app_ctx=app.app_context()
    #  app_ctx.push()
    #  print('current_app name :%s' % current_app.name)
    #  app.run(debug=True)
