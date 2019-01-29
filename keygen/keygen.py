import random
import string
from enum import Enum
import re

from keygen.model import Key, db

db.create_all()
db.session.commit()

chars = string.ascii_letters + string.digits


class KeyInfo(Enum):
    free = 'free'
    sent = 'sent'
    used = 'used'


def generate_key():
    if free_keys_left() == 0:
        return False

    key_str = generate_key_string(4)
    while key_exists(key_str):
        key_str = generate_key_string(4)

    key = Key(key_str)
    db.session.add(key)
    db.session.commit()
    return key_str


def validate_key(key_str):
    if key_str:
        match = re.match(r'[a-zA-Z0-9]{4}', key_str.strip())
        return match is not None


def set_key_used(key_str):
    if not key_str:
        return False

    key_str = key_str.strip()
    key = get_key(key_str)
    if key and not key.used:
        key.used = True
        db.session.add(key)
        db.session.commit()


def get_key_information(key_str):
    if not key_str:
        return False

    key_str = key_str.strip()
    if not key_exists(key_str):
        return KeyInfo.free
    else:
        key = get_key(key_str)
        if key.used:
            return KeyInfo.used
        else:
            return KeyInfo.sent


def free_keys_left():
    return (len(chars) ** 4) - keys_count()


def generate_key_string(length):
    return ''.join(random.choice(chars) for _ in range(length))


def key_exists(key_str):
    return Key.query.filter(Key.value == key_str).count() > 0


def keys_count():
    return Key.query.count()


def get_key(key_str):
    return Key.query.filter(Key.value == key_str).first()
