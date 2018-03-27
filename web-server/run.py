#!/usr/bin/env python

from config import queueConf
from azure.servicebus import ServiceBusService, Message, Queue
from flask import Flask, render_template, request, Response
import json

bus_service = ServiceBusService(
    service_namespace = queueConf['service_namespace'],
    shared_access_key_name = queueConf['saskey_name'],
    shared_access_key_value = queueConf['saskey_value'])

SUCCESS = Response(json.dumps({'success':True}), status=200, mimetype='application/json')

app = Flask(__name__)

state = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sendwork', methods=['POST'])
def sendwork():
    work = request.get_json()['work']
    
    bus_service.send_queue_message(queueConf['queue_name'], Message(work))
    return SUCCESS

@app.route('/currentstate', methods=['GET'])
def current_state():
    return json.dumps({"containers": state})

@app.route('/updatestate', methods=['PUT'])
def update_state():
    new_state = request.get_json()

    for container in state:
        if container['name'] == new_state['name']:
            container.update(new_state)
            return SUCCESS

    state.append(new_state)
    return SUCCESS

def getRequest(url):
    try:
        res = requests.get(url)
        return json.loads(res.text)
    except:
        return False



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)