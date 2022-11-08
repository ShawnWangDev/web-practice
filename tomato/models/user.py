from flask_login import UserMixin
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import func

from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)
    salt = db.Column(db.String(16), nullable=False)
    avatar = db.Column(db.LargeBinary, nullable=True)
    nickname = db.Column(db.String(32), nullable=True)
    phone = db.Column(db.String(11), nullable=True)
    email = db.Column(db.String(32), nullable=True)
    create_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=True)
    visable = db.Column(db.String(1), nullable=False, default="1")
    UniqueConstraint('username')

    def __repr__(self):
        return '<User %r>' % self.name