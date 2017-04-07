[参考博客](http://www.oschina.net/translate/serving-flask-with-nginx-on-ubuntu)

[腾讯云配置：Flask + uWSGI + Nginx](http://www.tuicool.com/articles/YzyuMnR2)

1. 申请主机和域名先

2. 登录刚才申请到的主机
 * ssh -l user_name _your_ip
 * [给公钥云主机](http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/001374385852170d9c7adf13c30429b9660d0eb689dd43a000)
 * [SSH远程登录](http://blog.csdn.net/wh_19910525/article/details/7585257)

3. 一台新的linux系统,看看有没有python和git,没有就装一下  

4. 安装pip3: sudo apt-get install python3-pip  

5. 安装git: sudo apt-get install git   

6. 安装virtualenv: sudo pip3 install virtualenv   

7. 安装nginx和uwsgi  
参考博客里的'里程碑#1',我在安装了nginx和uwsgi后没有出现,
是因为没有放行80端口,去到安全组那里新建一条规则放行80端口后访问主机外网地址，ok  
[flask + uwsgi 在调试过程中让python文件的更改自动重启uwsgi](https://segmentfault.com/a/1190000008446077)

8. supervisor  
放在keplerblog目录下吧,方便
文件路径:sudo ln -s /home/ubuntu/keplerblog/supervisor.conf /etc/supervisor/conf.d/
sudo service supervisor start

9. sites-avaliable 和 sites-enables  
[nginx 的 sites-available sites-enabled 文件夹区别](https://www.v2ex.com/t/168135)   
[写给Web开发人员看的Nginx介绍](http://blog.csdn.net/david_xtd/article/details/16967837)
