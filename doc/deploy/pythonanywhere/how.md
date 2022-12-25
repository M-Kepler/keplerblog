- 从 github 上下载你的文件, 或上传你的文件

- 创建环境

  ```s
  mkvirtualenv flaskenv --python=python3.5
  ```

- 激活虚拟环境

  ```s
  source ./virtualenvs/flaskenv/bin/active
  ```

- 安装插件

  ```s
  pip install -r requestments/requestments.txt
  ```

- mysql 数据库

  修改 app/config.py 的数据库连接 SQLALCHEMY_DATABASE_URI:

  - 原@localhost:3306 改为@YOURNAME.mysql.pythonanywhere-services.com:3306

    数据库名称也要相应的改为自己创建的数据库名称

- 不会改 wsgi, 然后我新建一个 flask 的 web 应用就有了 wsgi,然后直接改改这个就成了

- 好像也挺简单的, 可是部署后我的现在还不能发验证邮箱

---

1. 创建数据库
2. python manager.py db upgade
