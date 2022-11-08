from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.sql import func

from app import db


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    subject = db.relationship('Subject', backref=db.backref(
        'record', uselist=False), uselist=False)
    outline = db.Column(db.String(128), nullable=True)
    tomato_amount = db.Column(TINYINT(unsigned=True), nullable=False)
    tomato_duration = db.Column(TINYINT(unsigned=True), nullable=False)
    total_duration = db.Column(db.Interval, nullable=False)
    interference = db.Column(db.String(64), nullable=True)
    create_at = db.Column(db.DateTime, server_default=func.now())
    submit_finish_at = db.Column(db.DateTime, nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    finish_time = db.Column(db.DateTime, nullable=True)
    is_done = db.Column(db.Boolean, nullable=False, default=False)
    working_time_proportion = db.Column(
        db.Float(precision='5,4'), nullable=True)
    visable = db.Column(db.String(1), nullable=False, default="1")
    actual_duration = db.Column(db.Interval, nullable=True)

    def __repr__(self):
        return '<Record %r>' % self.name
