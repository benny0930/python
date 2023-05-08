import random
import time
import base
import db
import gc
import comic
import ptt
import actor
import KPythonBot
import requests
import threading
import autoShotUrl
import socket
import json
import socketio

sio = socketio.Client()
event = 'my_event'


@sio.event()
def my_response(data):
    # handle the message
    # sio.emit('my_event', {"cmd": "joinRoom", "roomId": 8888})
    print(data)



@sio.event
def connect():
    print('Connected to server')
    # sio.emit('login', {'account': 'test', 'password': 'Aa123123', 'bank_id': 5})


@sio.event
def server_response(data):
    print('Server response:', data)


@sio.event
def message(data):
    print('Message from server:', data)

@sio.event
def connect_error():
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


url = 'http://cf3_api.local:2021'
# url = 'wss://kyastws.nettry.info'
sio.connect(url, transports=["websocket"])
print('my sid is', sio.sid)
# time.sleep(3)
# url = url.format(uid=uid, token=token)
# sio.emit(event, {"cmd": "register", "userId": uid, "role": "T", "deviceVersion": "1.0","s_sid": sio.sid, "token": token})
sio.emit('login', {'account': 'test', 'password': 'Aa123123', 'bank_id': 5})

# time.sleep(3)
