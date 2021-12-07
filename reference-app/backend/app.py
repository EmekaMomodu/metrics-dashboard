from flask import Flask, request, jsonify

from flask_pymongo import PyMongo
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

app = Flask(__name__)
metrics = GunicornInternalPrometheusMetrics(app)

# static information as metric
metrics.info('backend_app_info', 'Backend Application info', version='1.0.0')

app.config['MONGO_DBNAME'] = 'example-mongodb'
app.config['MONGO_URI'] = 'mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb'

mongo = PyMongo(app)


@app.route('/')
def homepage():
    return "Hello World"


@app.route('/api')
def my_api():
    answer = "something"
    return jsonify(repsonse=answer)


@app.route('/star', methods=['POST'])
def add_star():
    star = mongo.db.stars
    name = request.json['name']
    distance = request.json['distance']
    star_id = star.insert({'name': name, 'distance': distance})
    new_star = star.find_one({'_id': star_id})
    output = {'name': new_star['name'], 'distance': new_star['distance']}
    return jsonify({'result': output})


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/403")
def status_code_403():
    status_code = 403
    raise InvalidUsage("Raising status code: {}".format(status_code), status_code=status_code)


@app.route("/404")
def status_code_404():
    status_code = 404
    raise InvalidUsage("Raising status code: {}".format(status_code), status_code=status_code)


@app.route("/500")
def status_code_500():
    status_code = 500
    raise InvalidUsage("Raising status code: {}".format(status_code), status_code=status_code)


@app.route("/503")
def status_code_503():
    status_code = 503
    raise InvalidUsage("Raising status code: {}".format(status_code), status_code=status_code)


if __name__ == "__main__":
    app.run()
