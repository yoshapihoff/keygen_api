import os

from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy, Model
from flask_sqlalchemy_caching import CachingQuery

from api import app, key_length

Model.query_class = CachingQuery
db = SQLAlchemy(app, session_options={'query_cls': CachingQuery})

# it's necessary to create a db
from .tables import *

with app.app_context():
    if not os.path.isfile('base.db'):
        db.create_all()

cache = Cache(app, config={'CACHE_TYPE': 'filesystem'})
