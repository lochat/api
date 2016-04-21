from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(db.Document):
    username = db.StringField(max_length=100, required=True, unique=True)
    email = db.EmailField(max_length=64, required=True)
    password_hash = db.StringField(max_length=128, required=True, unique=True)
    confirmed = db.BooleanField(default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.username

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def likes(self, scrap):
        scrap.likes += 1

    def deslikes(self, scrap):
        if scrap.likes >= 0:
            scrap.likes -= 1


class Scrap(db.Document):
    user = db.ReferenceField(User, reverse_delete_rule=db.CASCADE)
    content = db.StringField(max_length=500, required=True)
    likes = db.IntField(default=0)
