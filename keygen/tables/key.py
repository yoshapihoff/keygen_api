from ..model import db, key_length


class Key(db.Model):
    __tablename__ = 'keys'

    value = db.Column(db.String(key_length), primary_key=True)
    used = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Key(value='{self.value}', used='{self.used}')>"

    def __init__(self, value):
        self.value = value
        self.used = False
