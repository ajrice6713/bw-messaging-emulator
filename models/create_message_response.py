import datetime
import json
import uuid

from typing import Dict
from sms_counter import SMSCounter


class CreateMessageResponse: 
    def __init__(self, request):
        self.id = str(uuid.uuid4())
        self.owner = request['from']
        self.applicationId = request['applicationId']
        self.time = str(datetime.datetime.utcnow().isoformat())
        self.segmentCount = 1
        self.direction = 'out'

        if type(request['to']) is str:
            self.to = [request['to']]
        else:
            self.to = request['to']

        self.mfrom = request['from']
        if 'media' in request:
            self.media = request['media']
        if 'text' in request:
            self.text = request['text']
        if 'tag' in request:
            self.tag = request['tag']
        if 'priority' in request:
            self.priority = request['priority']
    
    def calculate_segments(self, message) -> int:
        count = SMSCounter.count(message)
        return count['messages']
   
    def to_json(self) -> str:
        dict_response = {
            'id': self.id,
            'owner': self.owner,
            'applicationId': self.applicationId,
            'time': self.time,
            'direction': self.direction,
            'to': self.to,
            'from': self.mfrom
        }
        
        if hasattr(self, 'media'): dict_response['media'] = self.media
        if hasattr(self, 'text'): 
            dict_response['text'] = self.text
            dict_response['segmentCount'] = self.calculate_segments(self.text)
        if hasattr(self, 'tag'): dict_response['tag'] = self.tag
        if hasattr(self, 'priority'): dict_response['priority'] = self.priority
        
        return json.dumps(dict_response)
