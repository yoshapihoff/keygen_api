import random
import string
from enum import Enum
import re

from flask_sqlalchemy_caching import FromCache

from keygen.model import Key, db, cache, key_length

_chars = string.ascii_letters + string.digits


class KeyInfo(Enum):
    free = 'free'
    sent = 'sent'
    used = 'used'


def generate_key():
    if free_keys_left() == 0:
        return False

    key_str = _generate_key_string(key_length)
    key_str = _fix_key_str(key_str)

    if key_str:
        key = Key(key_str)
        db.session.add(key)

    db.session.commit()

    return key_str


def validate_key(key_str):
    if key_str and len(key_str) == key_length:
        match = re.match(r'[a-zA-Z0-9]{key_length}', key_str.strip())
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
    return (len(_chars) ** key_length) - _keys_count()


def _fix_key_str(key_str):
    key_list = list(key_str)
    variants_with_one_variable_char = len(_chars) ** (key_length - 1)

    prefix = str()
    for i in range(key_length):
        chars = string.ascii_letters + string.digits
        query = Key.query.filter(Key.value.like(prefix + key_list[i] + '%'))
        while query.count() == variants_with_one_variable_char:
            chars = _chars.replace(key_list[i], '')
            if len(chars) == 0:
                key_list[i] = '_'
                break
            key_list[i] = random.choice(chars)

        prefix += key_list[i] if key_list[i] != '_' else key_str[i]

    if ''.join(key_list) == '_' * key_length:
        return

    for i in range(key_length):
        if key_list[i] == '_':
            key_list[i] = key_str[i]

    return ''.join(key_list)


def _generate_key_string(length):
    result = []
    for _ in range(length):
        result.append(random.choice(_chars))
    return result


def _key_exists(key_str):
    return Key.query.filter(Key.value == key_str).options(FromCache(cache)).scalar() is not None


def _keys_count():
    return Key.query.options(FromCache(cache)).count()


def _get_key(key_str):
    return Key.query.filter(Key.value == key_str).options(FromCache(cache)).first()
