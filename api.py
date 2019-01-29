from flask_api import FlaskAPI

app = FlaskAPI(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CACHE_TYPE'] = 'null'  # for debug

from requestHandler import RequestHandler as rh


@app.route("/", methods=['GET'])
def index():
    return rh.get_keys_left_count()


@app.route("/getkey", methods=['GET'])
def getkey():
    return rh.get_key()


@app.route("/keyinfo", methods=['GET'])
def keyinfo():
    return rh.get_key_info()


@app.route("/setkeyused", methods=['GET'])
def setkeyused():
    return rh.set_key_used()


@app.errorhandler(404)
def handle_error_404(error):
    return {'error': 404, 'description': error}


@app.errorhandler(500)
def handle_error_500(error):
    return {'error': 500, 'description': error}


if __name__ == '__main__':
    app.run(debug=True)
