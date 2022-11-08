from app import db
from models.user import User


def add(user: User):
    db.session.add(user)
    db.session.commit()


def get_by_id(id: int):
    return User.query.filter(User.id == id, User.visable == '1').first()


def get_by_username(username: str):
    return User.query.filter(User.username == username, User.visable == '1').first()


def update_password_by_username(user):
    u = User.query.filter(User.username == user.username,
                        User.visable == '1').first()
    u.salt = user.salt
    u.password = user.password
    db.session.commit()
