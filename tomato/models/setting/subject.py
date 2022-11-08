from sqlalchemy.sql import func

from app import db


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(32), nullable=False)
    record_sum = db.Column(db.Integer, default=0)
    background_image = db.Column(db.String(128), nullable=True)
    create_at = db.Column(db.DateTime, server_default=func.now())
    visable = db.Column(db.String(1), nullable=False, default="1")

    def __init__(self, user_id, name, category_id):
        self.user_id = user_id
        self.name = name
        self.category_id = category_id

    def __repr__(self):
        return '<Subject %r>' % self.name
