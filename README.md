[TOC]

# keplerblog

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&width=435&lines=The+five+boxing+wizards+jump+quickly)](https://git.io/typing-svg)

## 说明

- [博客测试地址](https://kepler.pythonanywhere.com)

- `python manage.py --help` 下有很多有用的命令

  ```s
  # 创建数据库
  # create database if not exists keplerblog;

  cd source/

  # 部署
  python manage.py deploy

  # 添加管理员
  python manage.py create_user

  # 生成测试数据
  python manage.py fake

  # 也可以单独构造用户、文章、评论测试数据
  # python manage.py userfake
  # python manage.py commonfake
  # python manage.py categoryfake

  # 创建账号
  python manage.py create_user

  # 查询全部用户
  python manage.py query_all
  ```

## 虚拟环境

```sh
# Python 3.9.5
python -m venv venvdir
source venvdir/bin/activate
pip install -r source/requirements/dev.txt

```

### 遇到的问题

- [Character set 'utf8' unsupported in python mysql connector](https://stackoverflow.com/questions/73244027/character-set-utf8-unsupported-in-python-mysql-connector)

  ```sh
  pip3 install mysql-connector-python==8.0.29
  ```

- [ModuleNotFoundError: No module named `flask._compat`](https://blog.csdn.net/Deng872347348/article/details/126304487)

- [Exception: Install 'email_validator' for email validation support.](https://blog.csdn.net/not_so_bad/article/details/120936176)

- [ImportError: cannot import name 'MigrateCommand' from 'flask_migrate'](https://blog.csdn.net/YZL40514131/article/details/122954381)

- [windows 安装 pycrypto](https://blog.csdn.net/hl156/article/details/124537767)

- [Python 踩坑系列之报错无 'winrandom' 模块](https://www.cnblogs.com/deliaries/p/13409571.html)

## 本地启动

```sh
cd source/
# python manage.py dev
python wsgi.py

```

## 部署

- [部署到 pythonanywhere](doc/deploy/pythonanywhere/README.md)
