# coding:utf-8
from werkzeug.utils import secure_filename
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand, upgrade
from app import create_app, db
from app.models import User, Role, Category

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
#  数据库更新迁移,就好像git一样做版本控制的

#  也可以写带参数的脚本
@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=True)


#  进入shell调试的时候每次都要导入db,models太麻烦了,
#  所以配置一下shell命令的上下文,就可以在shell里用了,不用每次都导入
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))




@manager.command
def test():
    pass


#  部署
@manager.command
def deploy():
    upgrade()
    Role.seed()
    Category.seed()


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

