#!/usr/bin/env python
import os
from pymongo import MongoClient
import time

def main():
    msg = os.environ['MESSAGE']
    container_name = os.environ['CONTAINER_NAME']
    mongo_uri = os.environ['DATABASE_URI']

    print("Got message ", msg)
    print("Container_name", container_name)
    print("connection: ", mongo_uri)

    client = MongoClient(mongo_uri)

    #Does not have to already exist
    db=client.containerstate

    #Create Container State

    new_state = {
        "name": container_name,
        "state": "InProgress"
    }

    db.containerstate.insert_one(new_state)

    #Do some work
    time.sleep(20)

    #Updating State
    db.containerstate.update_one({'name': container_name}, { '$set': {"state": "Done"}})

if __name__ == '__main__':
    main()



