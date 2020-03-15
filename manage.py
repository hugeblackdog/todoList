from app import create_app, db

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app.models import Role, User

app = create_app('production')
# app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, Role=Role, User=User, db=db)


@manager.command
def tests():
    '''执行测试用例'''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


# 初始化 Flask-Script、Flask-Migrate 和为 Python shell 定义的上下文。
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
