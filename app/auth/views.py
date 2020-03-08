from flask_login import login_user, logout_user, login_required

from . import auth
from .forms import RegisterationForm
from flask import render_template, redirect, url_for, flash

from .. import db
from ..models import User
from .forms import LoginForm


@auth.route('/')
def index():
    return render_template('auth/index.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            flash('用户登录成功')
            return redirect(url_for('auth.index'))
        else:
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('用户注销成功')
    return redirect(url_for('auth.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        flash('注册成功')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
