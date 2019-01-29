from flask_api import FlaskAPI
from flask import request

app = FlaskAPI(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from keygen import *


@app.route("/", methods=['GET'])
def index():
    return {'free_keys_left': free_keys_left()}


@app.route("/getkey", methods=['GET'])
def getkey():
    key_str = generate_key()
    return {'key': key_str}


@app.route("/keyinfo", methods=['GET'])
def keyinfo():
    key_str = request.args.get('key')
    if key_str:
        if validate_key(key_str):
            key_info = get_key_information(key_str)
            return {'key_information': key_info.value}
        else:
            return {'error': f'invalid key \'{key_str}\''}

    return {'error': 'you must specify the parameter \'key\''}


@app.route("/setkeyused", methods=['GET'])
def setkeyused():
    key_str = request.args.get('key')
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

    return {'error': 'you must specify the parameter \'key\''}


@app.errorhandler(404)
def handle_error_404(error):
    return {'error': 404, 'description': error}


@app.errorhandler(500)
def handle_error_500(error):
    return {'error': 500, 'description': error}


if __name__ == '__main__':
    app.run(debug=True)
