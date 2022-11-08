from sqlalchemy.sql import func

from app import db


class UploadFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    create_at = db.Column(
        db.DateTime, server_default=func.now(), nullable=False)
    visable = db.Column(db.String(1), nullable=False, default="1")

    def __init__(self,path,name) -> None:
        self.path=path
        self.name=name

    def __repr__(self):
        return '<Upload File %r>' % self.name