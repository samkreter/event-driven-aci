
from pymongo import MongoClient

from config import MONGDB_URI


client = MongoClient(MONGDB_URI)

#Does not have to already exist
db=client.containerstate

#Inserting
# for i in range(10):
#     test_container_state = {
#         "name": "test-" + str(i),
#         "state": "Inprogress"
#     }
#     db.containerstate.insert_one(test_container_state)

test_container_state = {
        "name": "test-1",
        "state": "Inprogress"
    }

#Updating
db.containerstate.update_one({'name': "test-0"}, { '$set': {"state": "Inprogress"}})

#Deleing
#db.containerstate.delete_many({"name": "test-1"})

docs = db.containerstate.find({})

for doc in docs:
    print(doc)

