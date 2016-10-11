[TOC]
# 1  结构
## 1.1 run.py
    用于启动一个服务器，它从包获得应用副本并运行，不会在生产环境中用到。
## 1.2 requestments.txt
    用于列出应用所以来的所有python包，分为生产依赖、开发依赖
## 1.3 config.py
    包含应用需要的大多数配置变量
## 1.4 instance/config.py
    数据库配置等东西全放到里面
## 1.5 app/__init__.py
    用于初始化应用并把所有其他的组件组合在一起
## 1.6 app/views.app
    定义了路由
## 1.7 app/models.py
    定义了应用的模型
## 1.8 app/static
    网站静态文件
## 1.9 manage.py
    外部脚本，通过shell来运行,用来测试吧


# 2  csrf
    扩站点请求保护
    避免来自其他地方的post请求,需要标记post请求的来源,以免视图函数也去处理这些请求
    所以，需要识别这些请求是当前服务器输出的ui页面的post请求,进行wsgi配置就行了

# 3  请求上下文
    request: 请求对象，封装在客户端发出的HTTP请求中的内容
    session: 用来保存存储请求之间需要记住的值的字典
    current_app: 当前程序的实例

# 4  WTF
wtf


# 5  数据库
[ORM框架:SQLAlchemy](http://docs.sqlalchemy.org/en/latest/contents.html)
## 5.1 mysql数据库
    pip install mysql-connector-python-rf
    RUI:mysql+mysqlconnector://username:password@server/db

## 5.2 数据库事件
    触发器:操作表的时候触发一些事件
    事件:可以这样啊,每次插入用户都默认初始化他的role_id为guests

## 5.3 数据库迁移
    其实就是一个版本控制的作用,比如需要更新表结构,或者需要迁移到新机器上,
    migrate会自动创建数据迁移脚本

# 6  蓝图
    蓝图就像app里的模块，将不同的功能划分到不同的蓝图里,所以，
    蓝图有自己独立的静态文件独立的views等文件

## 6.1 端点endpoint
    url_for():为了防止后期改动需要频繁更换url所以引入端点,
    如url_for('auth.index', *argv)那么对应的端点就是blueprint.index,

## 6.2 全程
    其实也简单,前面说蓝图就是将不同功能的划分到不同模块中，方便管理而已，
    在没有使用蓝图之前只是采用了工厂方法，将初始化app的部分包装在函数里,
    然后放到__init__.py里，这样app包下导入方便,把处理数据库的models独立出来,
    把配置config独立出来，把视图view独立出来,结构还是挺清晰的，不过随着views
    越写越长，维护起来就不太好了.
         所以换个蓝图来组织代码.
    1. 先按需要组织好文件,放在自定义的文件夹里,就是先把views或form放对位置,
    然后引用蓝图编辑__init__.py 把这个文件夹初始化成一个包
    2. 到app/这个主文件夹下的__init__.py去注册当初定义的蓝图
    3. 最重要的还是引入蓝图后访问的URL由'localhost:5500/about'变为了'/localhost:5500/main/about.html',
       使用了url_for('index')的也需要将改为url_for(main.index)
       弄了好久，一直提示说找不到endpoint，原来是因为我用了nav插件做导航栏，
       但是没将链接改为auth.index


# 7  登录登出




