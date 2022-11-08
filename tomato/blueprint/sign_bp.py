from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app import login_manager
from service import user_serv

sign_page = Blueprint('sign_page', __name__,
                    template_folder='templates')


login_manager.login_view = 'sign_page.signin'


@login_manager.user_loader
def load_user(user_id):
    return user_serv.get_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('sign_page.signin'))


class SigninForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(), Length(min=1, max=32)])
    password = PasswordField('password', validators=[
        DataRequired(), Length(min=1, max=32)])
    submit = SubmitField('sign in')


@sign_page.route('/in', methods=['GET', 'POST'])
def signin():
    tip = ''
    form = SigninForm()
    if form.validate_on_submit():
        db_user = user_serv.get_by_username(form.username.data)
        if db_user and db_user.password == user_serv.get_sha1(db_user.salt+form.password.data):
            login_user(db_user)
            return redirect(url_for('home_page.index'))
        tip = 'username or password wrong.'
        return render_template('sign/signin.html', title="Sign in", form=form, tip=tip)
    return render_template('sign/signin.html', title="Sign in", form=form, tip=tip)


@sign_page.route("/out")
@login_required
def logout():
    logout_user()
    return redirect("/")
