import os
import json

from datetime import datetime

from models.callback import Callback
from models.create_message_response import CreateMessageResponse
from utils.utils import datetime_to_float, float_to_datetime

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
    key_func=get_remote_address
    # default_limits=["60/minute"]
)

app.config['BASIC_AUTH_USERNAME'] = username
app.config['BASIC_AUTH_PASSWORD'] = password
app.config['BASIC_AUTH_REALM'] = 'api'

basic_auth = BasicAuth(app)

maxQueueTime = 15.0*60.0    # e.g. default 15 minute queue
rateLimit = 1              # mps
timeSlice = 1/10            # 100ms between messages

currentTime = datetime.now()
lastSendTime = currentTime
nextSendTime = float_to_datetime(datetime_to_float(currentTime) + maxQueueTime)
nextSendTime = float_to_datetime(datetime_to_float(currentTime) + maxQueueTime + 1000)


def send_callback(data):
    callback_object = Callback(data)
    return


def send(response_object):     
    global currentTime
    global lastSendTime 
    global nextSendTime

    print("----------")
    print(f'Max queue Time: {maxQueueTime}')
    print(f'Current Time: {currentTime}')
    print(f'Last Send Time: {lastSendTime}')
    print(f'Next Send Time: {nextSendTime}')
    print("----------")

    if datetime_to_float(nextSendTime) < (datetime_to_float(currentTime) + maxQueueTime) :
        currentTime = datetime.now()
        
        print("-----ERROR-----")
        print(f'Max queue Time: {maxQueueTime}')
        print(f'Current Time: {currentTime}')
        print(f'Last Send Time: {lastSendTime}')
        print(f'Next Send Time: {nextSendTime}')
        print(f'{datetime_to_float(nextSendTime)} < {datetime_to_float(currentTime) + maxQueueTime}')
        print("-----ERROR-----")

        return '429 error', 429
    else:
        currentTime = datetime.now()
        response = app.response_class(
            response=response_object.to_json(),
            status=202,
            mimetype='application/json'
        )
        nextSendTime = float_to_datetime(max(datetime_to_float(lastSendTime), datetime_to_float(currentTime) + timeSlice))
        lastSendTime = currentTime
        
        print("----------")
        print(f'New next Send Time: {nextSendTime}')
        print(f'New last Send Time: {lastSendTime}')
        print("----------")

        send_callback(response_object)
        return response


@app.route('/', methods=['GET'])
# @limiter.limit("5/minute", override_defaults=True)
@basic_auth.required
def status_check():
    data = {'message': 'hello world'}
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    print(f'Last Send Time: {lastSendTime}')
    return response


@app.route('/users/<userId>/messages', methods=['POST'])
# @limiter.limit("60/minute")
@basic_auth.required
def handle_message_request(userId):
    response_object = CreateMessageResponse(request=request.get_json())
    return send(response_object)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
