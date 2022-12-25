from app import db
from models.setting.category import Category


def get_all_by_user_id(user_id):
    return Category.query.filter(Category.user_id == user_id, Category.visable == '1').all()


def add(category: Category):
    db.session.add(category)
    db.session.commit()

def get_one_by_id_and_user_id(id: int, user_id: int):
    return Category.query.filter(Category.id == id, Category.user_id == user_id).first()