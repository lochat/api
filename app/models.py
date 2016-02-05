from . import db


class User(db.Document):
    name = db.StringField(max_length=100, required=True)
    password = db.StringField(max_length=20, required=True)
