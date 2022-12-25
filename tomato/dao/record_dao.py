from datetime import datetime, timedelta

from app import db
from models.record import Record


def add(record: Record):
    db.session.add(record)
    db.session.commit()


def get_all_by_user_id(user_id):
    return Record.query.filter(Record.user_id == user_id)

def get_all_by_subject_id_and_user_id(subject_id,user_id):
    return Record.query.filter(Record.subject_id==subject_id,Record.user_id==user_id)

def get_total_minutes_by_subject_id_and_user_id(subject_id, user_id):
    record_list=Record.query.filter(Record.subject_id == subject_id,
                        Record.user_id == user_id)
    total=timedelta(days=0,hours=0,minutes=0,seconds=0,milliseconds=0)
    for record in record_list:
        total=total+record.total_duration
    return total


def get_by_id(id, user_id) -> Record:
    return Record.query.filter(Record.id == id, Record.user_id == user_id).first()


def update_start_and_finish_time(record: Record):
    r = Record.query.filter(
        Record.id == record.id, Record.user_id == record.user_id).first()
    r.start_time = record.start_time
    r.finish_time = record.finish_time
    r.interference = record.interference
    r.actual_duration = record.actual_duration
    r.working_time_proportion = record.working_time_proportion
    r.is_done = True
    r.submit_finish_at = datetime.now()
    db.session.commit()


def get_not_finished_within_24_hours(user_id: int):
    current_time = datetime.now()
    return Record.query.filter(Record.user_id == user_id, Record.is_done == False, Record.visable == '1', Record.create_at > current_time-timedelta(days=1))\
        .all()


def get_24_hours_finished(user_id: int) -> Record:
    datetime_now_before_1_day = datetime.now()-timedelta(days=1)
    return Record.query.filter(Record.user_id == user_id, Record.is_done == True, Record.finish_time > datetime_now_before_1_day)\
        .order_by(Record.finish_time.desc()).all()
