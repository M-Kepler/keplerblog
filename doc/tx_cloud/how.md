[参考博客](http://www.oschina.net/translate/serving-flask-with-nginx-on-ubuntu)

1. 申请主机和域名先
2. 登录刚才申请到的主机
3. 一台新的linux系统,看看有没有python和git,没有就装一下
4. 安装pip3: sudo apt-get install python3-pip
5. 安装git: sudo apt-get install git
6. 安装virtualenv: sudo pip3 install virtualenv

7. 安装nginx和uwsgi
    参考博客里的'里程碑#1',我在安装了nginx和uwsgi后没有出现,
    是因为没有放行80端口,去到安全组那里新建一条规则放行80端口后访问主机外网地址，ok

8. supervisor
放在keplerblog目录下吧,方便
文件路径:sudo ln -s /home/ubuntu/keplerblog/supervisor.conf /etc/supervisor/conf.d/
sudo service supervisor start


