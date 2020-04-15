# nginx
sudo ln -s /home/m_kepler/keplerblog/deploy/keplerblog_nginx.conf /etc/nginx/sites-enabled
sudo service nginx restart

# uwsgi

# supervisor
sudo ln -s /home/m_kepler/keplerblog/deploy/supervisor.conf /etc/supervisor/conf.d/
sudo service supervisor restart
