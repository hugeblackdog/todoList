from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from app.models import Category


class AddTodoForm(FlaskForm):
    content = StringField(
        label='任务内容',
        validators=[DataRequired()],
        render_kw={
            "class": "form-control",
        }
    )
    category = SelectField(
        label='任务类型',
        coerce=int,
        render_kw={
            "class": "btn btn-default",
        }

        # 存的是id整形
        # choices=[(item.id, item.name) for item in Category.query.all()]
    )
    submit = SubmitField(
        label='添加任务',
        render_kw={
            "class": "btn btn-default",
        }
    )

    def __init__(self):
        super(AddTodoForm, self).__init__()
        categories = Category.query.all()
        if categories:
            self.category.choices = [(item.id, item.name) for item in
                                     categories]
        else:
            self.category.choices = [(-1, "请先创建分类")]


class EditTodoForm(FlaskForm):
    content = StringField(
        label='任务内容',
        validators=[DataRequired()]
    )
    category = SelectField(
        label='任务类型',
        coerce=int,
        # 存的是id整形
        # choices=[(item.id, item.name) for item in Category.query.all()]

    )
    submit = SubmitField(
        label='编辑任务',

    )

    def __init__(self):
        super(EditTodoForm, self).__init__()
        categories = Category.query.all()
        if categories:
            self.category.choices = [(item.id, item.name) for item in
                                     categories]
        else:
            self.category.choices = [(-1, "请先创建分类")]


class AddCategoryForm(FlaskForm):
    name = StringField(label='分类名称',
                       validators=[DataRequired()]
                       )
    submit = SubmitField(
        label='添加分类',
    )

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('该分类已存在')
