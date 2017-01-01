[TOC]

Query

print(obj.statement) # 返回对应的sql语句

## 1.
    a = db.session.query(User)
> 返回查询对象 sqlalchemy.orm.query.Query object #  select * from users;

    b = User.query
> 返回可迭代对象 flask_sqlalchemy.BaseQuery object #  select * from users;


## 2.filter & filter_by
>  返回对象app.models.User object

        # filter 要用User.name引用对象, 而且需要' == '
    c = User.query.filter(User.name == 'Huangjinjie').first()
        # filter_by 要用name引用对象, 而且需要' = '
    c1 = User.query.filter_by(name = 'Huangjinjie').first()

## 3.query的方法
    a = User.query.filter(User.id.between(1,20));

    dd = db.session.query(User).filter(User.name=='Huangjinjie').first()

    上↑下↓一样的,返回对象app.models.User object

    dd = User.query.filter(User.name='Huangjinjie').first()
    dd.property

<!-- #  a和b都有一样的方法 -->
b1 = b.all() # 返回一个list，每个User对象为元素
b2 = User.query.count() # 返回这个list中对象的数量

##  4.对name标签下的文章做分页
page_index = 9
category = Category.query.filter_by(name=name).first()
pagination = Post.query.filter(Post.category_id == category.id).order_by(
        Post.create_time.desc().pagina
        page_index, per_page = config.PER_POSTS_PER_PAGE,
        error_out = False
        )
posts= pagination.items

