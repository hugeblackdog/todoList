from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)

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

    def __repr__(self):
        return '<User % r>' % self.username


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role % r>' % self.name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
