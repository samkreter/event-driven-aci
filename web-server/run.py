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

@app.route('/')
def index():

    return SUCCESS

@app.route('/sendwork', methods=['POST'])
def sendwork():
    work = request.form.get('work'))
    bus_service.send_queue_message('taskqueue', work)
    return SUCCESS


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8000)