[TOC]

[博客测试地址](https://kepler.pythonanywhere.com)

# 1  结构

## 1.1 run.py
    用于启动一个服务器，它从包获得应用副本并运行，不会在生产环境中用到。

## 1.2 requestments
    你想啊，可能有的插件只在测试的时候才需要啊，所以不必要都加入到requestments中
    可以新建dev.txt文档，加上-r requestments.txt就可以继承这个里面的插件了
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
    https://my.oschina.net/lionets/blog/410973

    session: 用来保存存储请求之间需要记住的值的字典
    current_app: 当前程序的实例
    g:
    请求钩子?


# 4  WTF
    validate_* 可以自己定义Field 的校验,并且这个会自动被调用来进行校验


# 5  数据库
[ORM框架:SQLAlchemy](http://docs.sqlalchemy.org/en/latest/contents.html)

## 5.1 mysql数据库
    pip install mysql-connector-python-rf
    RUI:mysql+mysqlconnector://username:password@server/db
    不支持中文?


## 5.2 数据库事件
    触发器:操作表的时候触发一些事件
    事件:可以这样啊,每次插入用户都默认初始化他的role_id为guests

## 5.3 Flask-migrate
    需要注意：也要放入版本控制中
    正常操作步骤跟着狗书走就对了
    其实就是一个版本控制的作用,比如需要更新表结构,或者需要迁移到新机器上,
    migrate会自动创建数据迁移脚本
    定义好模型，应该是就可以进行数据库迁移的了，但是我在迁移的过程中，遇到
    几个错误:
    > 1. python manager.py db migrate -m "update"
        python manager.py upgrade 提示我的数据库没有up to date
    > 2. 提示我某张数据表已经存在? why？
    最后我删掉了数据库里的表和migration文件夹，按照狗书重新来了一遍就好了

## 5.4 sqlalchemy增删查改,错误
* sqlalchemy.exc.invalidRequestError这什么鬼错误，到处搜不到[答案](https://segmentfault.com/q/1010000005080603)

## 5.5 点击标签显示该标签对应的文章   
    正文的话只要显示post.category.name就可以了，然后做个连接url_for到视图
    接下来点击标签就是访问那个视图，然后就。。
TODO   
    很简单啊，在index.html里显示了当前post的标签了，所以点击的话就连接到category/<name>就可以了;
    然后这个category视图把查到的posts返回去显示出来就可以了,这里我又写了个html，我感觉是不是可以复用一下index↓

    ```select category.id, category.name, posts.title from posts, categorys where(posts.category_id = category.id);```   
    以上的多表查询有问题 应该在最后加上````and category.id=2````
    这样的多表查询语句用sqlalchemy怎么写?
    > posts = db.session.query(Post).join(Category)

    我是想用上面这种多表查询的方法来查询某tagname下的文章的,sql语句会写, 但是sqlalchemy怎么写就不懂   

    后来看人家的源码知道, 在写模型的时候, 表A的外键所链接的表B, 模型里backref参数的,我当时以为只是给外键所在的表A一个参数以便它
    来访问这个表B, 谁知道B也可以用参数去访问A，这样太方便了好吗，我不需要给B表新添字段让他去参照A，或者写个多表查询的语句了

    但是，，，不用查询的话我怎么做分页？


    还有，难道真的要添加个count字段？我想在视图里query出来，然后传过去



## 5.6
    http://blog.csdn.net/huoyuan_zh/article/details/7322160

## 5.6 密码散列
    werkzeug库的security可以进行散列密码的计算，
    generate_password_hash(passwd, method...)方法计算原始密码的散列值
    check_password_hash(hash,passed)方法检查给出的hash密码与明文密码是否相符
    由于密码是只写的，所以注册的时候怎么写入密码呢?user.passwd=form.passwd.data
    验证登录的时候看一下form.email.data对应的check_password_hash是不是True就可以了

## 5.6 SUMMERY
    主要还是要建好表的映射，当然还有数据库事件触发器、seed、staticmethod这些也要懂


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


# 7 发送确认邮件
## 7.1 app/email.py
       怎么使用falsk-email来发邮件?配置email.py的时候, 要注意导入上下文?顺便导入配置文件里的变量?

## 7.2 发送确认邮件
       注册函数那里实例化User后,根据用户的id生成token,然后执行email函数发送一个带token的连接给用户,
       用户点击这个确认链接后就会访问到'/confirm/<token>'这个视图,这个视图调用models里的confirm函数对用户进行校验,
       如果校验成功就把confirmed设置为1,我们可以根据这个值判断用户是否点击了确认邮件，
       如果没有点击(confirmed=0)可以限制哪些页面用户可以访问
       template那里的参数,我直接在里面写'/auth/email/'就会自动选取app/template/auth/...下的HTML了;

## 7.3 什么？令牌
    itsdangerous
    注册或找回密码的时候需要发一个确认连接，这个链接肯定是加密的是唯一的，就叫做令牌吧token
    如果点了我发过去的确认邮件，我就讲你的confirmed值设置为True
    token的过程是怎么样的？ 看models里的注释吧，写得挺清楚的

## 7.4 sqlalchemy是自动提交的
    一切就绪了,注册完后也会发送确认邮件了,但是我点击了确认邮件,confirmed字段却没有被设置为1.
    理论上，在config中设置了SQLALCHEMY_COMMIT_ON_TEARDOWN = True的话是会自动提交的,
    也就是只要db.session.add(self)就行,不需要db.session.commit(),结果发现我单词写错了!!!!!!!


# 8 [Flask-Login](http://www.cnblogs.com/agmcs/p/4445428.html)
[flask-qq-weibo登录](http://www.cnblogs.com/GresonFrank/archive/2013/11/13/python.html)

    还是看官方文档好啊，至少说的明白清楚,搞清楚 继承UserMixin, login_request @login_manager.user_loader回调函数

## 8.1 我的时间?
    moment插件? 注册时间? 怎么实现上次登录时间? 就是登录就显示时间而已。

# 9 帖子和评论
## 9.1 how?
    很简单啦其实，一样，只是数据库操作啊，前面也定义好了表了;
    一个posts和一个edit, template/posts页面

## 9.2 markdown? 左右
    就是那种啊，一边编辑，一般预览啊; 装了markdown插件，我还是不会写页面啊，尴尬，甚至连那些标签都不懂，，，，
    [那怎么做个编辑框啊?](https://segmentfault.com/q/1010000004406545)
    [editormd](http://blog.csdn.net/hj960511/article/details/53037618)

## 9.3 页面显示文章摘要啊,readmore？
    https://segmentfault.com/q/1010000003496839
    用jinja2的truncate过滤器过滤后在后面合适的位置添加'了解更多',其实只要添加这篇posts的链接就可以了

## 9.4 分页
    /main/views.py pagination
    bootstrap支持分页,导入就可以 {% from "bootstrap/pagination.html" import render_pagination %}

## 9.5 由于展示帖子部分很多是一样的
    我不可能每个页面都复制一大堆div啊什么的吧，所以我写了个宏，就是把原来index里展示帖子、右侧栏的部分剪切过去，传入posts、categorys参数就可以了
    {% macro show_posts(posts, categorys) %}
    然后在index.html 或category.html引入就可以了
    {% from "./includes/_macros.html" import show_posts as onshow %}
    {{ onshow(posts, categorys) }}

## 9.6 右侧显示该标签下的文章数量, category/name页面也显示侧栏
    我现在需要知道这个标签下有多少篇文章怎么办?难道在模型加上count字段？然后呢？
    终于解决了!!
    <!-- FIXME -->
    我试过很多方法:
    1. 可以在models里加个count字段, 然后做个触发器，只要一引用就更新,但是这样可以吗？
        这种似乎是最好的了,将count字段存放在表里，需要的时候就取出来, 这样比下面的方法好,不需要每次都执行查询
    2. 在views里写sqlalchemy的查询语句,然后将count传到template里,然后显示出来
        这里花了好多时间...我一直在看是不是我的sqlalchemy语句写错了?
        我在models添加@property方法返回count,然后在视图就可以category.count计算出来了,但是我理解错了
        比如:db.session.query(Post).filter(Post.category_id == Category_id).count()
        但是上面这个语句是错的,要知道Post.category_id 是一个反引用，所以↑返回的肯定是所有数据的count,
        我以为像那样,传入category对象然后判断category.id和post.category_id是否相等是可以的
    ,,,我肯定是没有理解sqlalchemy的语句, 需要的参数是什么?返回的是对象?可迭代对象?这些,所以自己一直在那里搞

    解决方法:jinja2的count过滤器就可以了.......,记得吧,做点击分类名然后只显示该分类下的文章,,,
    我那时候也以为需要做多表查询（看5.5）

# 导航栏
    本来用的是flask-nav的，但是好像用的不太好，所以就copy了别人的导航栏_navbar.html，然后在base.html中引入
## 固定导航栏
    <nav class="navbar navbar-default navbar-fixed-top" role="navigation">
    <!-- 在base.html的block head中加入padding就可以避免用fiexed-top的时候内容和导航栏重叠 -->
      <style>
        body{
          padding-top:70px;
        }
      </style>


# [样式Bootstrap](http://www.runoob.com/bootstrap/bootstrap-glyphicons.html)
  左侧9列正文，右侧3列显示个人信息和标签

  这阶段是套用了别人的，不过bootstrap始终方便，有空我找找自己喜欢的样式,我现在的导航栏太丑了


# [本地化时间](http://www.cnblogs.com/agmcs/p/4446589.html)
    {{ super() }}
    {{ moment.include_moment() }}
    {{ moment.lang("zh-CN") }} //配置显示的是中文
    {% endblock %}
    {{ moment(post.create_time).fromNow(refresh=True) }}
    {{ moment(post.create_time).format('YYYY年M月D日-HH:mm:ss') }}

# 时间轴
