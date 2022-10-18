# coding:utf-8

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    PER_POSTS_PER_PAGE = 8

    DB_HOST = "127.0.0.1:3306"
    DB_USER = "root"
    DB_PWD = "root"
    DB_NAME = "keplerblog"


class DevelopmentConfig(Config):
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
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{Config.DB_USER}:{Config.DB_PWD}@{Config.DB_HOST}/{Config.DB_NAME}?charset=utf8"
    # to deploy in pythonanywhere
    # SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://Kepler:rootyp@Kepler.mysql.pythonanywhere-services.com:3306/Kepler$keplerblog?charset=utf8"


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
