from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import func

from app import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(32), nullable=False)
    background_image = db.Column(db.String(128), nullable=True)
    create_at = db.Column(db.DateTime, server_default=func.now())
    visable = db.Column(db.String(1), nullable=False, default="1")
    subjects = db.relationship('Subject', backref='category')
    UniqueConstraint("name")

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name
