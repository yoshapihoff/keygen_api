import random
import string
from enum import Enum
import re

from flask_sqlalchemy_caching import FromCache

from keygen.model import Key, db, cache

_chars = string.ascii_letters + string.digits


class KeyInfo(Enum):
    free = 'free'
    sent = 'sent'
    used = 'used'


def generate_key():
    if free_keys_left() == 0:
        return False

    key_str = _generate_key_string(4)
    while _key_exists(key_str):
        key_str = _generate_key_string(4)

    key = Key(key_str)
    db.session.add(key)
    db.session.commit()
    return key_str


def validate_key(key_str):
    if key_str and len(key_str) == 4:
        match = re.match(r'[a-zA-Z0-9]{4}', key_str.strip())
        return match is not None


def set_key_used(key_str):
    if not key_str:
        return False

    key_str = key_str.strip()
    key = _get_key(key_str)
    if key and not key.used:
        key.used = True
        db.session.add(key)
        db.session.commit()


def get_key_information(key_str):
    if not key_str:
        return False

    key_str = key_str.strip()
    if not _key_exists(key_str):
        return KeyInfo.free
    else:
        key = _get_key(key_str)
        if key.used:
            return KeyInfo.used
        else:
            return KeyInfo.sent


def free_keys_left():
    return (len(_chars) ** 4) - _keys_count()


def _generate_key_string(length):
    return ''.join(random.choice(_chars) for _ in range(length))


def _key_exists(key_str):
    return Key.query.options(FromCache(cache)).filter(Key.value == key_str).count() > 0


def _keys_count():
    return Key.query.options(FromCache(cache)).count()


def _get_key(key_str):
    return Key.query.options(FromCache(cache)).filter(Key.value == key_str).first()
