# coding:utf-8

"""
配置
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    通用配置
    """
    URL_PREFIX = "/kepler"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    PER_POSTS_PER_PAGE = 8

    # pythonanywhere 数据库链接配置
    # db_user = "Kepler" # pythonanywhere 的用户名
    # db_pwd = "1155993577yypp"
    # db_host = f"{db_user}.mysql.pythonanywhere-services.com:3306"
    # db_name = f"{db_user}$wechat"

    # 本地数据库链接配置
    db_user = "root"
    db_pwd = "root"
    db_host = "127.0.0.1:3306"
    db_name = "keplerblog"
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://" + \
        f"{db_user}:{db_pwd}@{db_host}/{db_name}?charset=utf8"


class DevelopmentConfig(Config):
    """
    开发模式下的配置
    """
    DEBUG = True
    # 从系统环境变量设置
    # export MAIL_SERVER = 'test'
    # 查看是否设置成功: echo $MAIL_SERVER
    # 从系统环境变量引入
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_POST = 25
    MAIL_USERNAME = 'm_kepler@foxmail.com'
    MAIL_PASSWORD = 'xvildlkqqkklbbbj'
    FLASK_MAIL_SUBJECT_PREFIX = 'M_KEPLER'
    FLASK_MAIL_SENDER = MAIL_USERNAME
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_DEBUG = True
    ENABLE_THREADS = True


class TestingConfig(Config):
    """
    测试模式下的配置
    """
    pass


class ProductionConfig(Config):
    """
    生产模式下的配置
    """
    pass


config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
