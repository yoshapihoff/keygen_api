from keygen import *


class RequestHandler:
    @staticmethod
    def get_keys_left_count():
        return {'free_keys_left': free_keys_left()}

    @staticmethod
    def get_key():
        return {'key': generate_key()}

    @staticmethod
    def get_key_info(key_str):
        if key_str:
            if validate_key(key_str):
                key_info = get_key_information(key_str)
                return {'key_information': key_info.value}
            else:
                return {'error': f'invalid key \'{key_str}\''}

        return {'error': 'you must specify the parameter \'/keyinfo/your_key\''}

    @staticmethod
    def set_key_used(key_str):
        if key_str:
            if validate_key(key_str):
                key_info = get_key_information(key_str)
                if key_info == KeyInfo.sent:
                    set_key_used(key_str)
                    return {'result': f'key \'{key_str}\' marked as used'}
                else:
                    already_word = 'already ' if key_info == KeyInfo.used else ''
                    return {'error': f'key \'{key_str}\' {already_word}marked as \'{key_info.value}\''}
            else:
                return {'error': f'invalid key \'{key_str}\''}

        return {'error': 'you must specify the parameter \'/setkeyused/your_key\''}
