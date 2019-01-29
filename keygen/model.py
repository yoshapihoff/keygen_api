import os

from api import app
from flask_sqlalchemy import SQLAlchemy, Model
from flask_sqlalchemy_caching import CachingQuery
from flask_caching import Cache

Model.query_class = CachingQuery
db = SQLAlchemy(app, session_options={'query_cls': CachingQuery})


class Key(db.Model):
    __tablename__ = 'keys'

    value = db.Column(db.String(4), primary_key=True)
    used = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Key(value='{self.value}', used='{self.used}')>"

    def __init__(self, value):
        self.value = value
        self.used = False


with app.app_context():
    if os.path.isfile('base.db'):
        db.create_all()

cache = Cache(app)
