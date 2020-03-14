from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import Length, DataRequired, EqualTo, ValidationError


class editUserInfoForm(FlaskForm):
    username = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('用户住址', validators=[Length(0, 64)])
    about_me = TextAreaField('自我介绍')
    submit = SubmitField('更改资料')


class changePasswordForm(FlaskForm):
    oldPassword = PasswordField('旧密码', validators=[Length(0, 64),
                                                   DataRequired()],
                                render_kw={
                                    'placeholder': '旧密码'
                                })
    newPassword = PasswordField('旧密码', validators=[Length(0, 64),
                                                   DataRequired()],
                                render_kw={
                                    'placeholder': '新密码'
                                })
    rePassword = PasswordField('旧密码', validators=[Length(0, 64),
                                                  DataRequired(),
                                                  EqualTo('newPassword', message='密码不一致')],
                               render_kw={
                                   'placeholder': '确认密码'
                               })
    submit = SubmitField('更改密码')

    def validate_oldPassword(self, field):
        if not current_user.verify_password(field.data):
            print(field.data)
            raise ValidationError('原密码不正确')

    def validate_newPassword(self, field):
        if current_user.verify_password(field.data):
            raise ValidationError('新密码不能与原密码一致')
