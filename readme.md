- [博客测试地址](https://kepler.pythonanywhere.com)，测试账号: Admin@test.com 密码: 123456

- 文档在 `keplerblog/doc` 下

- `manage.py` 下有很多有用的命令  
  ```s
  # 部署
  python manage.py deploy
  # 添加管理员
  python manage.py create_user
  # 生成测试数据
  python manage.py fake
  python manage.py userfake
  python manage.py commonfake
  python manage.py categoryfake
  # 查询全部用户
  python manage.py query_all
  ```
