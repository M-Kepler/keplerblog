# coding:utf-8

"""
控制台命令

python manage.py --help

命令的注释将会作为帮助信息展示出来

"""

import unittest

from app import create_app
from app.models.category import Category
from app.models.comment import Comment
from app.models.post import Post
from app.models.role import Role
from app.models.user import User
from app.plugins import db
from flask_migrate import Migrate, MigrateCommand, upgrade
from flask_script import Manager, Shell
from livereload import Server

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    """
    进入shell调试的时候每次都要导入db,models太麻烦了,
    所以配置一下shell命令的上下文,就可以在shell里用了,不用每次都导入
    """
    return dict(app=app,
                db=db,
                User=User,
                Role=Role,
                Post=Post,
                Comment=Comment,
                Category=Category)


@manager.command
def dev():
    """
    启动，修改代码后，会自动刷新页面
    """
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url_delay=True)


@manager.command
def test():
    """
    单元测试
    """
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def query_all():
    """
    查询全部用户
    """
    users = User.query.all()
    for item in users:
        print(f"User Name: \t{item.name}")
        print(f"User Email: \t{item.email}")
        print(f"Register Time: \t{item.register_time}")
        print("=" * 40)


@manager.command
def fake():
    """
    生成测试数据
    """
    User.generate_fake()
    Category.generate_fake()
    Post.generate_fake()
    Comment.generate_fake()


@manager.command
def fake_user():
    """
    生成测试用户
    """
    User.generate_fake()


@manager.command
def fake_post():
    """
    生成测试文章
    """
    Post.generate_fake()


@manager.command
def fake_comment():
    """
    生成测试评论
    """
    Comment.generate_fake()


@manager.command
def fake_category():
    """
    生成测试分类
    """
    Category.generate_fake()


@manager.option('-u', '--name', dest='name')
@manager.option('-e', '--email', dest='email')
@manager.option('-p', '--password', dest='password')
def create_user(name, email, password):
    """
    添加默认管理员
    """
    if name is None:
        name = input('Username(default admin):') or 'admin'
    if email is None:
        email = input('Email:')
    if password is None:
        password = input('Password:')
    user = User()
    user.name = name
    user.password = password

    user.email = email
    user.is_administrator = True
    user.confirmed = 1
    role = Role.query.filter_by(name='administrators').first()
    if role is None:
        role = Role()
        role.name = 'administrators'
    user.role = role
    db.session.add(user)
    db.session.commit()


@manager.command
def deploy():
    """
    一键部署
    """
    upgrade()
    Role.seed()
    Category.seed()


@manager.option('-u', '--name', dest='name')
def reset_pwd(name):
    """
    重置密码
    """
    user = User.query.filter_by(name=name).first()
    user.password = "1234567"
    db.session.add(user)
    print(f"重置 {name} 密码成功")


# 也可以用这种方式添加命令
manager.add_command(
    "shell",
    Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()
    # 程序上下文
    # app_ctx=app.app_context()
    # app_ctx.push()
    # print('current_app name :%s' % current_app.name)
    # app.run(debug=True)
