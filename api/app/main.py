import datetime
import os
from time import sleep

from fastapi import FastAPI
import pymongo
from bson import json_util
import json

sleep(30)
db_client = pymongo.MongoClient(os.environ["MONGO_URL"])
print(db_client.list_database_names())
db = db_client["chat_db"]

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "API"}


@app.post("/send/{room_id}/{message}")
async def send_message(room_id: str, message: str):
    room = db[f"room{room_id}"]

    insert_message = {
        "author": "anonymous",
        "message": message,
        "timestamp": datetime.datetime.utcnow()
    }

    room.insert_one(insert_message)
    return json_util.dumps(insert_message)


@app.get("/getn/{room_id}/{no_msg}")
async def get_n_messages(room_id: str, no_msg: int):
    room = db[f"room{room_id}"]
    msg_cursor = room.find().sort("timestamp", pymongo.DESCENDING).limit(no_msg)
    return json_util.dumps(msg_cursor)
