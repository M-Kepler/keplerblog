- step1. 下载代码

  ```sh
  # 切换到 dev 分支
  git clone git@github.com:M-Kepler/keplerblog.git -b dev
  ```

- step2. 创建虚拟环境，并安装依赖

  安装过程在遇到的问题见 [按照过程遇到的问题](../../../README.md#遇到的问题)

  ```sh
  cd keplerblog
  python -m venv venvdir
  source venvdir/bin/activate
  pip install -r source/requirements/dev.txt

  ```

- step3. 修改配置文件

  - 修改 `app/config.py/Config/SQLALCHEMY_DATABASE_URI` 数据库连接配置

  - 创建或修改 `/var/www/kepler_pythonanywhere_com_wsgi.py` 内容为 [kepler_pythonanywhere_com_wsgi](kepler_pythonanywhere_com_wsgi.py)

- step4. 创建数据表

  ```sh
  1. 创建数据库
  2. python manager.py db upgade
  ```

- step5. 测试一下数据库链接

  ```sh
  python manage.py query_all

  ```

- step6. 本地跑一下

  ```sh
  python manage.py runserver
  ```

- step7. 配置 pythonanywhere 的 web 页面
