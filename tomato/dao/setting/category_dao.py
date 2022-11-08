from app import db
from models.setting.category import Category


def get_all(user_id):
    return Category.query.filter(Category.user_id == user_id, Category.visable == '1').all()


def add(category: Category):
    db.session.add(category)
    db.session.commit()

def get_by_id(id: int, user_id: int):
    return Category.query.filter(Category.id == id, Category.user_id == user_id).first()