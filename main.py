import os
import json

from models.callback import Callback
from models.create_message_response import CreateMessageResponse

from rich import print, inspect

from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_basicauth import BasicAuth

username = os.environ['BW_USERNAME']
password = os.environ['BW_PASSWORD']


app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["60/minute"]
)
app.config['BASIC_AUTH_USERNAME'] = username
app.config['BASIC_AUTH_PASSWORD'] = password
app.config['BASIC_AUTH_REALM'] = 'api'
basic_auth = BasicAuth(app)


def send_callback(data):
    callback_object = Callback(data)
    return


@app.route('/', methods=['GET'])
@limiter.limit("5/minute", override_defaults=True)
@basic_auth.required
def status_check():
    data = {'message': 'hello world'}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/users/<userId>/messages', methods=['POST'])
@limiter.limit("60/minute")
@basic_auth.required
def handle_message_request(userId):
    response_object = CreateMessageResponse(request=request.get_json())

    response = app.response_class(
        response=response_object.to_json(),
        status=202,
        mimetype='application/json'
    )

    send_callback(data=response_object)

    return response


if __name__ == '__main__':
    app.run(port=5000, debug=True)
