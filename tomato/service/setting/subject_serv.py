import dao.setting.subject_dao as subject_dao
from models.setting.subject import Subject


def get_all(user_id: int):
    return subject_dao.get_all(user_id)


def get_by_id(id: int, user_id: int):
    return subject_dao.get_by_id(id, user_id)


def add(user_id: int, name: str, category_id: int):
    subject = Subject(user_id, name, category_id)
    subject_dao.add(subject)
