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


DATETIME_FORMAT = r'%Y/%m/%d %H:%M'


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
    outline = TextAreaField('outline', validators=[Length(max=128)])
    now = datetime.now()
    record_id = HiddenField()
    interference = TextAreaField('interference', validators=[Length(max=64)])
    start_time = DateTimeField('start time', validators=[
        InputRequired()], format=DATETIME_FORMAT)
    finish_time = DateTimeField('finish time', validators=[
        InputRequired()], format=DATETIME_FORMAT)
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
        start_time = datetime.now().replace(second=0, microsecond=0)
        # a person cannot create a record at 0 second time(such as 17:05:00)
        # then start the tomato immediately at 17:05:00.
        # so delay one minute(+timedelta(minutes=1)).
        if start_time == record.create_at.replace(second=0, microsecond=0):
            start_time = start_time+timedelta(minutes=1)
        rec_dt = RecordDatetime(start_time, tomato_minutes)
        form.start_time.data = start_time
        form.finish_time.data = rec_dt.expected_finish_time
    # POST
    if request.method == 'POST':
        start_time = form.start_time.data
        finish_time = form.finish_time.data
        create_time = record.create_at.replace(second=0, microsecond=0)
        rec_dt = RecordDatetime(start_time, tomato_minutes)
        # valid conditon 1:
        #   actual working duration equals or greater than total tomato duration
        #   actual working duration less than one day
        # valid condition 2:
        #   submitted start time greater than create time of the record
        if not (rec_dt.is_actual_duration_valid(finish_time) and start_time > create_time):
            return redirect(url_for('record_page.enter', record_id=rid))
        record.start_time = rec_dt.start_time
        record.finish_time = rec_dt.finish_time
        record.actual_duration = rec_dt.actual_duration
        record.working_time_proportion = rec_dt.working_duration_proportion()
        record.interference = form.interference.data
        record_serv.update_finished(record)
        return redirect(url_for('record_page.doday_finished'))
    return render_template('record/enter.html', title='Do it!', form=form, record=record, record_datetimes=rec_dt)


@record_page.route('today_finished')
@login_required
def today_finished():
    records = record_serv.get_today_finished(current_user.id)
    return render_template('record/today_finished.html', title='today finished', records=records)


@record_page.route('update/<record_id>', methods=['GET', 'POST'])
@login_required
def update(record_id):
    rid = escape(record_id)
    user_id = current_user.id
    record = record_serv.get_by_id(rid, user_id)
    tomato_minutes = record.tomato_amount*record.tomato_duration
    form = EnterRecordForm()
    form.record_id = rid
    if request.method == 'GET':
        form.interference.data = record.interference
        form.outline.data = record.outline
        form.interference.data = record.interference
        form.start_time.data = record.start_time
        form.finish_time.data = record.finish_time
        form.submit.data = 'update'
        rec_dt = RecordDatetime(record.start_time, tomato_minutes)
        return render_template('record/update.html', title='update', form=form, record=record, record_datetimes=rec_dt)
    # POST
    if request.method == 'POST':
        start_time = form.start_time.data
        finish_time = form.finish_time.data
        rec_dt = RecordDatetime(start_time, tomato_minutes)
        is_actual_duration_valid=rec_dt.is_actual_duration_valid(finish_time)
        if not (is_actual_duration_valid and start_time > record.create_at):
            return redirect(url_for('record_page.update', record_id=rid))
        record.interference = form.interference.data
        record.outline = form.outline.data
        record.start_time = rec_dt.start_time
        record.finish_time = rec_dt.finish_time
        record.actual_duration = rec_dt.actual_duration
        record.working_time_proportion = rec_dt.working_duration_proportion()
        record_serv.update_start_and_finish_time(record)
        return redirect(url_for('record_page.today_finished'))
