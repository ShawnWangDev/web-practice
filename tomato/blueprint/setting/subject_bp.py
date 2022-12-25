from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

import service.setting.category_serv as category_serv
import service.setting.subject_serv as subject_serv

subject_page = Blueprint('subject_page', __name__,
                        template_folder='templates')


class SubjectForm(FlaskForm):
    name = StringField('name', validators=[
        DataRequired(), Length(min=1, max=32)])
    category_list = SelectField(
        'categories', validators=[DataRequired()], coerce=int)
    submit = SubmitField('add the subject')


@subject_page.route('/')
@login_required
def subject_index():
    subjects = subject_serv.get_all_by_user_id(current_user.id)
    return render_template('setting/subject/index.html', title="subject", subjects=subjects)


@subject_page.route('/add', methods=['GET', 'POST'])
@login_required
def subject_add():
    form = SubjectForm()
    category_list = [(int(c.id), c.name)
                    for c in category_serv.get_all_by_user_id(current_user.id)]
    form.category_list.choices = category_list
    if form.validate_on_submit():
        subject_serv.add(current_user.id, form.name.data,
                        form.category_list.data)
        return redirect(url_for('subject_page.subject_index'))
    return render_template('setting/subject/add.html', title='add a subject', form=form)
