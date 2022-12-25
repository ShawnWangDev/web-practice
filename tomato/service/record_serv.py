from datetime import timedelta

import dao.record_dao as record_dao
import dao.setting.subject_dao as subject_dao
from models.record import Record


def add(user_id: int, subject_id: int, outline: str, amount: int, duration: int, total_duration: timedelta):
    record = Record()
    record.user_id = user_id
    record.subject_id = subject_id
    record.outline = outline
    record.tomato_amount = amount
    record.tomato_duration = duration
    record.total_duration = total_duration
    record_dao.add(record)

def get_all_by_user_id(user_id):
    return record_dao.get_all_by_user_id(user_id)

def get_total_minutes_by_subject_id_and_user_id(subject_id, user_id):
    return record_dao.get_total_minutes_by_subject_id_and_user_id(subject_id,user_id)

def get_by_id(id, user_id) -> Record:
    return record_dao.get_by_id(id, user_id)


def get_current(user_id):
    return record_dao.get_not_finished_within_24_hours(user_id)


def get_24_hours_finished(user_id: int) -> Record:
    return record_dao.get_24_hours_finished(user_id)


def update_finished(record):
    subject_dao.record_amount_increment_one(record.subject_id, record.user_id)
    record_dao.update_start_and_finish_time(record)

def update_start_and_finish_time(record):
    record_dao.update_start_and_finish_time(record)

def get_tomato_info(record_id: int, user_id: int) -> Record:
    return record_dao.get_tomato_info(record_id, user_id)
