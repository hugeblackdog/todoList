from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length


class editUserInfoForm(FlaskForm):
    username = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('用户住址', validators=[Length(0, 64)])
    about_me = TextAreaField('自我介绍')
    submit = SubmitField('更改资料')
