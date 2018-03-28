#!/usr/bin/env python

from config import queueConf, DATABASE_URI
from azure.servicebus import ServiceBusService, Message, Queue
from flask import Flask, render_template, request, Response
import json
from pymongo import MongoClient

#set up the service bus queue
bus_service = ServiceBusService(
    service_namespace = queueConf['service_namespace'],
    shared_access_key_name = queueConf['saskey_name'],
    shared_access_key_value = queueConf['saskey_value'])

#Connect to the databases
client = MongoClient(DATABASE_URI)
db = client.containerstate

#Preset respones
SUCCESS = Response(json.dumps({'success':True}), status=200, mimetype='application/json')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sendwork', methods=['POST'])
def sendwork():
    work = request.get_json()['work']

    print("Creating job with work: ", work)

    bus_service.send_queue_message(queueConf['queue_name'], Message(work))
    return SUCCESS


@app.route('/clear', methods=['PUT'])
def clear():
    print("clearing database")
    db.containerstate.delete_many({})
    return SUCCESS


@app.route('/currentstate', methods=['GET'])
def current_state():
    #Get all container states
    container_states = db.containerstate.find({})

    current_states = []

    #Convert to list of state objects
    for state in container_states:
        current_states.append({
            "name": state['name'],
            "state": state['state']
        })

    return json.dumps({"container_states": current_states})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)