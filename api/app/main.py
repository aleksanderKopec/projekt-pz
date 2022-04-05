import base64
import binascii
import datetime
import os
from time import sleep
import conn_managers

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
import pymongo
from bson import json_util
from typing import Union, List
import json


db_manager = conn_managers.DBManager(os.environ["MONGO_URL"])

# db_client = pymongo.MongoClient(os.environ["MONGO_URL"])
# db = db_client["chat_db"]
# channel_id_db = db["channel_id"]

app = FastAPI()
channel_manager = conn_managers.ChannelManager(db_manager)


@app.get("/")
async def root():
    return {"message": "API"}


@app.get("/api/{channel_id}")
async def get_messages(channel_id: str, message_id: int | None, number_of_messages: int = 10):

    channel, _ = await db_manager.get_channel(channel_id)

    messages = channel\
        .find({"message_id": {"$lte": message_id}})\
        .sort("timestamp", pymongo.DESCENDING)\
        .limit(number_of_messages)
    return json_util.dumps(messages)


@app.websocket("/ws/{channel_id}")
async def ws_chat(websocket: WebSocket, channel_id: str, username: str):
    _, channel_no = await db_manager.get_channel(channel_id)
    channel = channel_manager.get_channel(channel_no)
    await channel.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = {
                "message_id": await db_manager.get_last_message_no(channel_no) + 1,
                "author": username,
                "message": data,
                "timestamp": f"{datetime.datetime.utcnow().isoformat()}"
            }
            db_manager.db[f"room_{channel_no}"].insert_one(message)

            await channel.broadcast(f"{message}")

    except WebSocketDisconnect:
        channel.disconnect(websocket)
        await channel.broadcast(f"Client #{username} left the chat")
