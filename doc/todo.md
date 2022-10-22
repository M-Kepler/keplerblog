- [TODO](#todo)
- [DEPLOY PROBLEM](#deploy-problem)
- [FINISH](#finish)
- [已完成](#已完成)
- [TIPS](#tips)

- 20171209

  这个博客项目最糟糕的一点就是那个编辑器了，
  [这个的编辑器好多了](https://github.com/flyhigher139/OctBlog)

# TODO

- [x] √ 归档界面没有适应移动端哦
- [x] √ 首页在移动端显示的时候两边太宽了
- [x] √ 修改 manager.py 设置默认角色和默认管理,也不知道现在那个 fake 还能不能用
- [x] 文档写两份:本地测试 + pythonanywhere.com 部署
- [ ] 页脚呢?
- [ ] 在管理那里加一个一键备份功能吧,考虑下用 git
- [ ] 接入社交化评论
- [ ] 做测试
- [ ] flask-admin
- [ ] flask-restful
- [ ] flask-celery
- [ ] flask-cache
- [ ] 要不要结合 autocompelte 呢?自动补全已有标签

# DEPLOY PROBLEM

- 为什么部署后无法收到邮件?

# FINISH

- [x] ☆ 评论没做分页、且不可以回复、评论不可以 markdown 预览、发表评论后希望能看到我的评论
- [x] 部署后确认链接没有发送成功,config 问题？
- [x] 用户个人信息页也太简单了吧,改为可以看 md，不可以更改
- [x] fake 还能用,就是不能给 posts 加上 category
- [x] 全文搜索
- [x] 文章阅读量显示
- [x] 更新密码
- [x] 重置密码\更换邮箱

# 已完成

- [x] √ 输入可添加 category 的测试,详见 main.view.py
- [x] √ 数据库多对多的测试, 详见 model.py
- [x] √ 可以用,分隔输入多个标签了
- [x] √ 3.5 就差 bootstrap-tagsinput 或 tokenfields
- [x] ☆ 就是输入,后显示成标签的样子,如果已经有这个分类就选择不用创建
- [x] √ 文章和分类改为多对多
- [x] 可以插入,找到一篇文章的所有标签,某个标签下的所有文章了
- [x] √ 更改 model,所以比如无法在 index.html 正确显示标签、右侧栏标签后的数字显示
- [x] 出错都弄好了 python manager.py shell 真好用
- [x] √ 可以编辑个人资料,管理员可以编辑其他用户的资料
- [x] √ 还没做分类删除
- [x] √ 可以自适应了,是一个 div 的设置问题
- [x] √ 加入了轮播,但没找合适的图片

# TIPS

- 记得关掉调试模式, 启动脚本为 flask_app.py
- 记得敏感信息从系统环境引入
