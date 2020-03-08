from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from app.models import User


class RegisterationForm(FlaskForm):
    email = StringField(u'电子邮箱', validators=[
        DataRequired(), Length(1, 20),
        Email(message=u'邮箱格式不正确')
    ])
    username = StringField('用户名', validators=[
        DataRequired(), Length(1, 15),
        Regexp('^\w*$', message='用户名只能以字母数字或者下划线开头')
    ])
    password = PasswordField('密码', validators=[
        DataRequired()
    ])
    repassword = PasswordField('确认密码', validators=[
        DataRequired(), EqualTo('password', message='密码不一致')

    ])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            # 自定义的验证函数要想表示验证失败,可以抛出 ValidationError 异常,其参数就是错误消息。
            raise ValidationError('电子邮箱已经注册.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经占用.')


class LoginForm(FlaskForm):
    email = StringField(u'电子邮箱', validators=[
        DataRequired(), Length(1, 20),
        Email(message=u'邮箱格式不正确')
    ])
    password = PasswordField('密码', validators=[
        DataRequired()
    ])
    submit = SubmitField('注册')
