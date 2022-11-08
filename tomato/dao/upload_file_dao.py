from app import db
from models.upload_file import UploadFile


def add(upload_file: UploadFile):
    db.session.add(upload_file)
    db.session.commit()


def get_by_id(id: int):
    return UploadFile.query.filter(UploadFile.id == id, UploadFile.visable == '1').first()
