from . import auth
from .forms import RegisterationForm
from flask import render_template, redirect, url_for, flash

from .. import db
from ..models import User


@auth.route('/')
def index():
    return 'index'


@auth.route('/login')
def login():
    return 'login'


@auth.route('/logout')
def logout():
    return 'logout'


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
