import base64
import binascii
import datetime
import os
from time import sleep

from fastapi import FastAPI, HTTPException, WebSocket
import pymongo
from bson import json_util
from typing import Union
import json

sleep(30)
db_client = pymongo.MongoClient(os.environ["MONGO_URL"])
print(db_client.list_database_names())

db = db_client["chat_db"]
channel_id_db = db["channel_id"]

app = FastAPI()


async def get_channel(channel_id: str):
    # validate base64
    try:
        base64.b64decode(channel_id)
    except binascii.Error:
        raise HTTPException(status_code=500, detail=f"Channel ID not b64 encoded")

    channel_id_no = channel_id_db.find_one({"channel_id": channel_id})
    if channel_id_no is None:
        channel_no = channel_id_db.find_one(sort=[("channel_id", pymongo.DESCENDING)])["channel_no"] + 1
        channel_id_no = {"channel_id": channel_id, "channel_no": channel_no}
        channel_id_db.insert_one(channel_id_no)

    channel_no = channel_id_db["channel_no"]
    channel = db[f"room_{channel_no}"]
    return channel


@app.get("/")
async def root():
    return {"message": "API"}


@app.get("/api/{channel_id}")
async def get_messages(channel_id: str, message_id: Union[int, None], number_of_messages: int):

    channel = await get_channel(channel_id)

    messages = channel\
        .find({"message_id": {"$lte": message_id}})\
        .sort("timestamp", pymongo.DESCENDING)\
        .limit(number_of_messages)
    return json_util.dumps(messages)


@app.websocket("/ws/{channel_id}")
async def ws_chat(websocket: WebSocket, channel_id: str, username: str):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(data)


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
