from datetime import datetime

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from flask_login import UserMixin

'''
角色：用户 1：N
用户：任务 1：N
用户：分类 1：N
分类：任务 1：N
'''


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(200))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    # 用户的真实姓名
    location = db.Column(db.String(64))  # 所在地
    about_me = db.Column(db.Text())  # 自我介绍

    # 注册日期
    # default 参数可以接受函数作为默认值,
    # 所以每次生成默认值时,db.Column() 都会调用指定的函数。
    create_time = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    todos = db.relationship('Todo', backref='user')
    categories = db.relationship('Category', backref='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        # generate_password_hash(password, method= pbkdf2:sha1 , salt_length=8):密码加密的散列值。
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # check_password_hash(hash, password) :密码散列值和用户输入的密码是否匹配.
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        # 先生成一个加密器
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'],
                                            expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        # 必须使用相同的SECRET_KEY，否则无法解密
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception as e:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def ping(self):
        # 更新最后一次访问时间
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return '<User % r>' % self.username


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role % r>' % self.name


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    content = db.Column(db.String(100))
    # 任务内容
    status = db.Column(db.Boolean, default=False)
    # 任务的状态
    add_time = db.Column(db.DateTime, default=datetime.utcnow)
    # 用户：任务 1：N
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 分类：任务 1：N
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return "<Todo %s>" % (self.content[:6])


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    add_time = db.Column(db.DateTime, default=datetime.utcnow)
    # 用户：分类 1：N
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    todos = db.relationship('Todo', backref='category')

    def __repr__(self):
        return "<Category %s>" % (self.name)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
