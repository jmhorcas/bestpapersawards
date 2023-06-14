
from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, Document):
    id = IntField(primary_key=True)
    username = StringField(max_length=64, unique=True)
    email = StringField(max_length=120, unique=True)
    password_hash = StringField(max_length=128)

    def __repr__(self):
        return f"<User {self.username}>"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


def get_user(email: str):
    return User.objects(email=email).first()