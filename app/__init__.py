from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from config import config
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()


def create_app(config_name='development'):
    """
    默认创建开发环境的app对象
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    # 附加路由和自定义的错误页面
    # .........后续还需完善, 补充视图和错误页面
    from app.auth import auth
    app.register_blueprint(auth)

    from app.todo import todo
    app.register_blueprint(todo, url_prefix='/todo')

    login_manager.init_app(app)

    return app
