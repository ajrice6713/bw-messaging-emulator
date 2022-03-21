import os
import json

from datetime import datetime, timedelta

# from models.callback import Callback
from models.create_message_response import CreateMessageResponse
from utils.utils import datetime_to_float, float_to_datetime

from flask import Flask, request
from flask_basicauth import BasicAuth

username = os.environ['BW_USERNAME']
password = os.environ['BW_PASSWORD']

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = username
app.config['BASIC_AUTH_PASSWORD'] = password
app.config['BASIC_AUTH_REALM'] = 'api'

basic_auth = BasicAuth(app)

maxQueueTime = 15.0*60.0                      # e.g. default 15 minute queue
rateLimit = 1                                 # mps
timeSlice = timedelta(seconds=(1/rateLimit))  # 100ms between messages

currentTime = datetime.now()
lastSendTime = currentTime
nextSendTime = 0.0


# def send_callback(data):
#     callback_object = Callback(data)
#     return


def send(response_object):     
    global currentTime
    global lastSendTime 
    global nextSendTime

    currentTime = datetime.now()
    nextSendTime = (max(lastSendTime, currentTime)) + timeSlice
    print(f'nextSendTime: {nextSendTime}')
    
    if nextSendTime > float_to_datetime(datetime_to_float(currentTime) + maxQueueTime) :
        return '429 error', 429
    else:
        currentTime = datetime.now()
        response = app.response_class(
            response=response_object.to_json(),
            status=202,
            mimetype='application/json'
        )
        lastSendTime = nextSendTime
        # send_callback(response_object)
        return response


@app.route('/', methods=['GET'])
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
@basic_auth.required
def handle_message_request(userId):
    response_object = CreateMessageResponse(request=request.get_json())
    return send(response_object)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
