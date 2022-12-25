import dao.setting.subject_dao as subject_dao
import dao.record_dao as record_dao
from models.setting.subject import Subject


def get_all_by_user_id(user_id: int):
    return subject_dao.get_all_by_user_id(user_id)


def get_all_by_user_id_orderby_record_sum_desc(user_id):
    subject_query = subject_dao.get_all_by_user_id(user_id)
    subject_list = []
    for s in subject_query:
        subject_list.append(s)
    subject_list.sort(key=lambda x: x.record_sum, reverse=True)
    return subject_list


class Subject_Info:
    def __init__(self, subject_id, category_name, subject_name, total_time):
        self.subject_id = subject_id
        self.category_name = category_name
        self.subject_name = subject_name
        self.total_time = total_time


def all_info_get_by_user_id(user_id):
    subject_list = get_all_by_user_id_orderby_record_sum_desc(user_id)
    info_list = []
    for s in subject_list:
        total = record_dao.get_total_minutes_by_subject_id_and_user_id(
            s.id, user_id)
        info = Subject_Info(s.id, s.category.name, s.name, total_time=total)
        info_list.append(info)
    return info_list


def get_all_by_category_id_and_user_id(id: int, user_id: int):
    return subject_dao.get_all_by_category_id_and_user_id(id, user_id)


def add(user_id: int, name: str, category_id: int):
    subject = Subject(user_id, name, category_id)
    subject_dao.add(subject)
