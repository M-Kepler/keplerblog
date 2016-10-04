# coding:utf-8
from werkzeug.utils import secure_filename
from flask.ext.script import Manager, Shell
from app import create_app, db
from app.models import User

app = create_app()
manager = Manager(app)

#  也可以写带参数的脚本
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
def deploy():
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


if __name__ == '__main__':
    manager.run()
    # 程序上下文
    #  app_ctx=app.app_context()
    #  app_ctx.push()
    #  print('current_app name :%s' % current_app.name)
    #  app.run(debug=True)

