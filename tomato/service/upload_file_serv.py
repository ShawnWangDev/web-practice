import dao.upload_file_dao as upload_file_dao
from models.upload_file import UploadFile


def add(upload_file: UploadFile):
    upload_file_dao.add(upload_file)

def get_by_id(id):
    return upload_file_dao.get_by_id(id)

def get_by_username(name:str):
    return upload_file_dao.get_by_username(name)
