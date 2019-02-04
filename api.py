from flask_api import FlaskAPI
from flask import send_from_directory
import os

app = FlaskAPI(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CACHE_TYPE'] = 'filesystem'

cache_path = './cache_temp/'

if not os.path.exists(cache_path):
    os.makedirs(cache_path)
app.config['CACHE_DIR'] = cache_path

from requestHandler import RequestHandler as Handler


@app.route("/", methods=['GET'])
def index():
    return Handler.get_keys_left_count()


@app.route("/getkey", methods=['GET'])
def getkey():
    return Handler.get_key()


@app.route("/keyinfo/", defaults={'key': None})
@app.route("/keyinfo/<string:key>")
def keyinfo(key):
    return Handler.get_key_info(key)


@app.route("/setkeyused/", defaults={'key': None})
@app.route("/setkeyused/<string:key>")
def setkeyused(key):
    return Handler.set_key_used(key)


@app.errorhandler(404)
def handle_error_404(error):
    return {'error': 404, 'description': error}


@app.errorhandler(500)
def handle_error_500(error):
    return {'error': 500, 'description': error}


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(debug=False)
