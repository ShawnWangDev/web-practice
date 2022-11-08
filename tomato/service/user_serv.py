import hashlib
import random

import dao.user_dao as user_dao
from models.user import User


def generateRandChar(n):
    result = []
    sample = '0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()-+=.'
    for i in range(n):
        char = random.choice(sample)
        result.append(char)
    return ''.join(result)


def get_sha1(text):
    hash_sha1 = hashlib.sha1()
    hash_sha1.update(text.encode('utf-8'))
    return hash_sha1.hexdigest()


def get_by_id(id):
    return user_dao.get_by_id(id)


def get_by_username(username: str):
    return user_dao.get_by_username(username)


def add_user_with_username_password(username: str, password: str):
    user = User()
    user.username = username
    user.salt = generateRandChar(16)
    user.password = get_sha1(user.salt+password)
    user_dao.add(user)


def update_password_by_username(username: str, password: str):
    user = User()
    user.username = username
    user.salt = generateRandChar(16)
    user.password = get_sha1(user.salt+password)
    user_dao.update_password_by_username(user)
