import dao.setting.category_dao as category_dao
from models.setting.category import Category


def get_all_by_user_id(user_id: int):
    return category_dao.get_all_by_user_id(user_id)


def add(user_id: int, name: str):
    category = Category(user_id, name)
    category_dao.add(category)


def get_one_by_id_and_user_id(id: int, user_id: int):
    return category_dao.get_one_by_id_and_user_id(id, user_id)
