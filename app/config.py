#cofing:utf-8
'''
/***********************************************************
* Author       : M_Kepler
* EMail        : hellohuangjinjie@gmail.com
* Last modified: 2016-10-10 08:43:19
* Filename     : config.py
* Description  :
**********************************************************/
'''
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    #  从系统环境变量中获取敏感信息
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLAlCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER=os.environ.get('MAIL_SERVER')
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    MAIL_PORT=25
    MAIL_USE_TLS=True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:159357@localhost:3306/micblog"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:159357@localhost:3306/micblog"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:159357@localhost:3306/micblog"

config = {
        'development' : DevelopmentConfig,
        'testing' : TestingConfig,
        'production' : ProductionConfig,
        'default' : DevelopmentConfig
        }
