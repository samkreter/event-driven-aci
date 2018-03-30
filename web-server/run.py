#!/usr/bin/env python

from config.config import queueConf, DATABASE_URI, ACI_CONFIG, azure_context
from azure.servicebus import ServiceBusService, Message, Queue
from azure.monitor import MonitorClient
from flask import Flask, render_template, request, Response
import json
import sys
from pymongo import MongoClient
from bson.json_util import dumps

#The monitor client to get container group metrics
monitor_client = MonitorClient(azure_context.credentials, azure_context.subscription_id)

#set up the service bus queue
bus_service = ServiceBusService(
    service_namespace = queueConf['service_namespace'],
    shared_access_key_name = queueConf['saskey_name'],
    shared_access_key_value = queueConf['saskey_value'])

#Connect to the databases
client = MongoClient(DATABASE_URI + "&ssl=true")
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

@app.route('/admin/currentdbstate', methods=['GET'])
def current_db_state():
    db_state = db.containerstate.find({})
    return dumps({"db_state": list(db_state)})


@app.route('/api/availablemetrics/<container_name>', methods=['GET'])
def available_metrics(container_name):
    resource_id = (
        "subscriptions/{}/"
        "resourceGroups/{}/"
        "/providers/microsoft.containerinstance/containerGroups/{}"
    ).format(ACI_CONFIG['subscriptionId'], ACI_CONFIG['resourceGroup'], container_name)

    metrics = monitor_client.metric_definitions.list(resource_id)

    available_metrics = [ metric.name.value for metric in metrics]

    return json.dumps({"available_metrics": available_metrics})


@app.route('/api/metrics/<container_name>', methods=['GET'])
def get_metrics(container_name):
    metrics = _get_metrics(ACI_CONFIG['subscriptionId'], ACI_CONFIG['resourceGroup'], container_name)

    print(metrics)

    return json.dumps({"chartData": metrics})


def _get_metrics(subscription_id, resource_group_name, container_name):
    resource_id = (
        "subscriptions/{}/"
        "resourceGroups/{}/"
        "/providers/microsoft.containerinstance/containerGroups/{}"
    ).format(subscription_id, resource_group_name, container_name)

    #filter = " and ".join(["name.value"])CpuUsage,MemoryUsage

    labels = []
    series_labels = []
    data_points = []
    
    metrics_data = monitor_client.metrics.list(resource_id, metric='MemoryUsage')
    for item in metrics_data:
        data = list()
        series_label = list()

        labels.append(item.name.value)

        for data_point in item.data:
            data.append(NoneZero(data_point.average))
            series_label.append(data_point.time_stamp.strftime('%H:%M:%S'))

        series_labels.append(series_label)
        data_points.append(data)

    return {
        "labels": labels,
        "seriesLabels": series_labels,
        "dataPoints": data_points
    }


def NoneZero(val):
    if val is None:
        return 0
    else:
        return val

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)