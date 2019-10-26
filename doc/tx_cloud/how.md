- [参考博客](http://www.oschina.net/translate/serving-flask-with-nginx-on-ubuntu)

- [腾讯云配置：Flask + uWSGI + Nginx](http://www.tuicool.com/articles/YzyuMnR2)

- 申请主机和域名先

- 登录刚才申请到的主机

- ssh -l user_name \_your_ip
- [给公钥云主机](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/001374385852170d9c7adf13c30429b9660d0eb689dd43a000)
- [SSH 远程登录](http://blog.csdn.net/wh_19910525/article/details/7585257)

- 一台新的 linux 系统,看看有没有 python 和 git,没有就装一下

- 安装 pip3: sudo apt-get install python3-pip

- 安装 git: sudo apt-get install git

- 安装 virtualenv: sudo pip3 install virtualenv

- 安装 nginx 和 uwsgi  
  参考博客里的'里程碑#1',我在安装了 nginx 和 uwsgi 后没有出现,
  是因为没有放行 80 端口,去到安全组那里新建一条规则放行 80 端口后访问主机外网地址，ok  
  [flask + uwsgi 在调试过程中让 python 文件的更改自动重启 uwsgi](https://segmentfault.com/a/1190000008446077)

- supervisor  
  放在 keplerblog 目录下吧,方便
  文件路径:sudo ln -s /home/ubuntu/keplerblog/supervisor.conf /etc/supervisor/conf.d/
  sudo service supervisor start

- sites-avaliable 和 sites-enables  
  [nginx 的 sites-available sites-enabled 文件夹区别](https://www.v2ex.com/t/168135)  
  [写给 Web 开发人员看的 Nginx 介绍](http://blog.csdn.net/david_xtd/article/details/16967837)
