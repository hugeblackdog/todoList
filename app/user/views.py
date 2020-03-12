from flask_login import current_user, login_required

from app import db
from app.models import User
from app.user import user
from flask import abort, render_template, flash, redirect, url_for

from app.user.forms import editUserInfoForm


@user.route('/user/<id>')
@login_required
def get_userInfo(id):
    user = User.query.filter_by(id=id).first()
    print(user)
    if not user:
        abort(404)
    else:
        if user != current_user:
            abort(404)
        return render_template('user/user.html')


@user.route('/editInfo', methods=['GET', 'POST'])
def edit_Info():
    form = editUserInfoForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('用户信息修改成功', category='success')
        return redirect(url_for('user.get_userInfo', id=current_user.id))
    form.username.data = current_user.username
    form.location = current_user.location
    form.about_me = current_user.about_me
    return render_template('user/edit_profile.html', form=form)
