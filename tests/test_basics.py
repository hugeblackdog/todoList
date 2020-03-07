import unittest
from flask import current_app
from app import create_app, db


class basicsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        # 将当前的app的属性信息与当前实例绑定
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        # Pops the app context
        self.app_context.pop()

    def test_app_exists(self):
        """测试当前app是否存在?"""

        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """测试当前app是否为测试环境?"""

        self.assertTrue(current_app.config['TESTING'])
