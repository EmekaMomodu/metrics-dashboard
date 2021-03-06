from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import pymongo
import logging
from flask_pymongo import PyMongo
from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter import jaeger
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics
# from os import getenv
# JAEGER_HOST = getenv('JAEGER_HOST', 'localhost')


# Configure Jaeger tracer
def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
            # 'local_agent': {'reporting_host': JAEGER_HOST}
        },
        service_name=service,
        validate=True
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


tracer = init_tracer('backend-service')

app = Flask(__name__)

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
CORS(app)

metrics = GunicornInternalPrometheusMetrics(app, group_by='endpoint')

# static information as metric
metrics.info('backend_app_info', 'Backend Application info', version='1.0.0')

# register extra metrics
metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths', labels={'path': lambda: request.path}
    )
)

# custom metric to be applied to multiple endpoints
endpoint_counter = metrics.counter(
    'by_endpoint_counter', 'Request count by endpoints',
    labels={'endpoint': lambda: request.endpoint}
)

app.config['MONGO_DBNAME'] = 'example-mongodb'
app.config['MONGO_URI'] = 'mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb'

mongo = PyMongo(app)


@app.route('/')
@endpoint_counter
def homepage():
    with tracer.start_active_span('home-page'):
        answer = "Hello World, its the Home Page !"
        return jsonify(response=answer)


@app.route('/api')
@endpoint_counter
def my_api():
    with tracer.start_span('my-api'):
        answer = error  # Error line
        return jsonify(response=answer)


@app.route('/star', methods=['POST'])
@endpoint_counter
def add_star():
    with tracer.start_span('add star'):
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
