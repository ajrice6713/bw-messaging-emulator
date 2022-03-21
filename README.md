# bw-messaging-emulator

A flask API to test Bandwidth's Messaging API Rate Limit Logic

## Getting Started 

```sh
mkdir bw-emulator
git clone https://github.com/ajrice6713/bw-messaging-emulator bw-emulator
cd bw-emulator

# without using pipenv 
pip install -r requirements.txt 
python main.py

# with pipenv
pipenv install
pipenv run python main.py
```

The server will start on `localhost:5000`. 

### Mocking a Message 

You can now test the rate lmit logic using your http client of choice 

```http
POST /users/<userId>/messages HTTP/1.1
Host: localhost:5000
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
Content-Type: application/json

{
    "to"            : "+19195551234",
    "from"          : "+19195554321",
    "text"          : "This is a test message from Bandwidth.",
    "applicationId" : "9414cd25-720b-43ae-9e45-33f4a3f283f3",
    "tag"           : "test message",
    "priority"      : "default"
}
```

*NOTE*: No logic or enforcememt is in place to check for any configuration errors with your to/from numbers, credentials, or application ID. Nothing is written and this application creates a completely unique service entirely independent of Bandwidth, meant for local testing of Bandwidth's Messaging API rate limit logic. This application does not trigger any callbacks or validate whether or not a message would be successfully passed off to the downstream carrier - it assumes that your messages are formatted correctly and simply checks against the rate limit assigned to your account and either returns a `200` or a `429` response. 

## Configuration

The app is set by default to replicate Bandwidhts 1mps and 15 min queue

You can configure custom limits by changing the following parameters in `main.py` 

```python
maxQueueTime = 15.0*60.0    # e.g. default 15 minute queue
rateLimit = 1               # mps
```
