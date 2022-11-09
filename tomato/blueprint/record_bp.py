from datetime import datetime, timedelta

from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from markupsafe import escape
from wtforms import (DateTimeField, HiddenField, IntegerField, SelectField,
                     SubmitField, TextAreaField)
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange

import service.record_serv as record_serv
import service.setting.category_serv as category_serv
import service.setting.subject_serv as subject_serv

from models.record_datetime import RecordDatetime

record_page = Blueprint('record_page', __name__,
                        template_folder='templates')


class RecordForm(FlaskForm):
    outline = TextAreaField('outline', validators=[Length(max=128)])
    category_list = SelectField('category', validators=[
        DataRequired()], coerce=int)
    subject_list = SelectField('subject', validators=[
        DataRequired()], coerce=int)
    tomato_amount = IntegerField('tomato amount', validators=[
        DataRequired(), NumberRange(min=1, max=16, message='numeric limited')])
    tomato_duration = IntegerField('tomato duration', validators=[
        DataRequired(), NumberRange(min=1, max=360, message='numeric limited')])
    submit = SubmitField('add record')


class EnterRecordForm(FlaskForm):
    datetime_format = r'%Y/%m/%d %H:%M'
    now = datetime.now()
    record_id = HiddenField()
    interference = TextAreaField('interference', validators=[Length(max=64)])
    start_time = DateTimeField('start time', validators=[
        InputRequired()], format=datetime_format, default=now)
    finish_time = DateTimeField('finish time', validators=[
        InputRequired()], format=datetime_format)
    submit = SubmitField('finish!')


@record_page.route('/')
@login_required
def current():
    records = record_serv.get_current(current_user.id)
    return render_template('record/current.html', title="current tomatoes", records=records)


@record_page.route('add', methods=['GET', 'POST'])
@login_required
def add():
    form = RecordForm()
    if request.method == 'GET':
        user_id = current_user.id
        category_list = []
        for c in category_serv.get_all(user_id):
            category_list.append((int(c.id), c.name))
        subject_list = []
        for s in subject_serv.get_by_id(category_list[0][0], user_id):
            subject_list.append((int(s.id), s.name))
        form.category_list.choices = category_list
        form.subject_list.choices = subject_list
    elif request.method == 'POST':
        record_serv.add(current_user.id, form.subject_list.data,
                        form.outline.data,
                        form.tomato_amount.data,
                        form.tomato_duration.data,
                        timedelta(minutes=form.tomato_amount.data*form.tomato_duration.data))
        return redirect(url_for('record_page.current'))
    return render_template('record/add.html', title='add a tomato', form=form)


@record_page.route('enter/<int:record_id>', methods=['GET', 'POST'])
@login_required
def enter(record_id):
    form = EnterRecordForm()
    rid = escape(record_id)
    form.record_id = rid
    user_id = current_user.id
    record = record_serv.get_by_id(rid, user_id)
    tomato_minutes = record.tomato_amount*record.tomato_duration
    # GET
    if request.method == 'GET':
        # not allow user to enter the finished tomato record if the record had done
        # redirect to 'add record' page if the user visiting finished record
        if record.is_done == True:
            return redirect(url_for('record_page.add'))
        start_time = datetime.now()
        finish_time = datetime.now()+timedelta(minutes=tomato_minutes)
        form.start_time.data = start_time
        form.finish_time.data = finish_time
        rec_dt = RecordDatetime(start_time, finish_time, tomato_minutes)
    # POST
    if request.method == 'POST':
        start_time = form.start_time.data
        finish_time = form.finish_time.data
        create_time = record.create_at.replace(second=0, microsecond=0)
        rec_dt = RecordDatetime(start_time, finish_time, tomato_minutes)
        # valid conditon 1:
        #   actual working duration equals or greater than total tomato duration
        #   actual working duration less than one day
        # valid condition 2:
        #   submitted start time greater than create time of the record
        if not (rec_dt.is_actual_duration_valid() and start_time > create_time):
            return redirect(url_for('record_page.enter', record_id=rid))
        record.start_time = rec_dt.start_time
        record.finish_time = rec_dt.finish_time
        record.actual_duration = rec_dt.actual_duration
        record.working_time_proportion = rec_dt.working_duration_proportion()
        record.interference = form.interference.data
        record_serv.update_finished(record)
        return redirect(url_for('record_page.finished'))
    return render_template('record/enter.html', title='Do it!', form=form, record=record, record_dateimes=rec_dt)


@record_page.route('finished')
@login_required
def finished():
    records = record_serv.get_finished(current_user.id)
    return render_template('record/finished.html', title='finished', records=records)
