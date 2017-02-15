#cofing:utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    PER_POSTS_PER_PAGE=8
    #  @staticmethod
    #  def init_app(app):
        #  pass

class DevelopmentConfig(Config):
    DEBUG = True
    #  MAIL_SERVER = os.environ.get('MAIL_SERVER')
    #  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    #  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_USERNAME = 'm_kepler@foxmail.com'
    MAIL_PASSWORD = 'xvildlkqqkklbbbj'
    FLASK_MAIL_SUBJECT_PREFIX='M_KEPLER'
    FLASK_MAIL_SENDER=MAIL_USERNAME
    MAIL_PORT=25
    MAIL_USE_TLS=True
    MAIL_DEBUG = True
    ENABLE_THREADS=True
    #  SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:159357@localhost:3306/keplerblog"
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:159357@localhost:3306/keplerblog?charset=utf8"
    #  to deploy in pythonanywhere
    #  SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://Kepler:159357yp@Kepler.mysql.pythonanywhere-services.com:3306/Kepler$keplerblog?charset=utf8"

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

