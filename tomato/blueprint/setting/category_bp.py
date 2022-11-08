import json

from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from markupsafe import escape
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

import service.setting.category_serv as category_serv

categrory_page = Blueprint('categrory_page', __name__,
                        template_folder='templates')


class CategoryForm(FlaskForm):
    name = StringField('name', validators=[
        DataRequired(), Length(min=1, max=32)])
    submit = SubmitField('add the category')


@categrory_page.route('/')
@login_required
def categrory_index():
    categories = category_serv.get_all(current_user.id)
    return render_template('setting/category/index.html', title="category", categories=categories)


@categrory_page.route('/add', methods=['GET', 'POST'])
@login_required
def category_add():
    form = CategoryForm()
    if form.validate_on_submit():
        category_serv.add(current_user.id, form.name.data)
        return redirect(url_for('categrory_page.categrory_index'))
    return render_template('setting/category/add.html', title='add a caetegory', form=form)


@categrory_page.route('/get/<int:id>')
@login_required
def get_by_id(id):
    id = escape(id)
    category = category_serv.get_by_id(id, current_user.id)
    subject_list = []
    for subject in category.subjects:
        subject_dict = {}
        subject_dict['id'] = subject.id
        subject_dict['name'] = subject.name
        subject_list.append(subject_dict)
    return json.dumps(subject_list)
