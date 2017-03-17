* 初始化
```
python manager.py db init
# 最后出现...before proceeding为成功
```

* 创建迁移脚本
```
python manager.py db migrate -m "init"
# 最后出现...done为成功
```

* 部署
```
python manager.py deploy
```

* 创建管理员
```
python manager create_user
```

* 生成fake数据
```
python manager fake
> python manger postfake （userfake\commentfake\categoryfake）
```

*

