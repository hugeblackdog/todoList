import os

# 获取当前文件目录的绝对路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # os.environ可以读取linux中的SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'westos secret key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PRE_PAGE = 5
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = '25'
    # MAIL_USE_TLS = True
    MAIL_USERNAME = '15094087934@163.com'

    MAIL_PASSWORD = 'centos123'

    @staticmethod
    def init_app(self):
        pass


class DevelopmentConfig(Config):
    """
    开发环境的配置信息
    """
    # 启用了调试支持,服务器会在代码修改后自动重新载入,并在发生错误时提供一个相当有用的调试器。
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data-dev.sqlite')


class TestingConfig(Config):
    """
    测试环境的配置信息
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data-test.sqlite')


class ProductionConfig(Config):
    """
    生产环境的配置信息
    """
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PRE_PAGE = 5
    # MAIL_SERVER = 'smtp.163.com'
    # MAIL_PORT = '465'
    # MAIL_USE_SSL = True
    # MAIL_USE_TLS = False
    # MAIL_USERNAME = '15094087934@163.com'
    # MAIL_PASSWORD = 'centos123'
    MAIL_SERVER = 'smtp.aliyun.com'
    MAIL_PORT = '25'
    MAIL_USE_TLS = True
    # MAIL_USE_SSL = True
    MAIL_USERNAME = 'todolist@aliyun.com'
    MAIL_PASSWORD = 'Sc135790'

    SQLALCHEMY_DATABASE_URI = 'mysql://flask:centos@101.132.41.88/todoList'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
