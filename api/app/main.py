import datetime
import os
from time import sleep
from model.model import MessageModel, MessagesModel
import conn_managers

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
import pymongo
from bson import json_util
from typing import Union, List
import json

app = FastAPI()

db_manager = conn_managers.DBManager(os.environ["MONGO_URL"])
channel_connection_manager = conn_managers.ChannelConnectionManager(db_manager)


@app.get("/")
async def root():
    return {"message": "API"}


@app.get("/api/{channel_id}", response_model=MessagesModel)
async def get_messages(channel_id: str, message_id: int | None = None, number_of_messages: int | None = None):
    channel = db_manager.get_channel(channel_id)

    if number_of_messages is not None:
        messages = db_manager.get_messages(channel, number_of_messages)
    else:
        messages = db_manager.get_messages(channel, 10)

    return MessagesModel(channel_id=channel_id, messages=messages)


@app.websocket("/ws/{channel_id}")
async def ws_chat(websocket: WebSocket, channel_id: str, username: str):
    channel = db_manager.get_channel(channel_id)
    connection = channel_connection_manager.get_channel_connection(channel_id)

    await connection.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = MessageModel(
                message_no=db_manager.get_next_message_no(channel),
                author=username,
                message=data,
                timestamp=f"{datetime.datetime.utcnow().isoformat()}"
            )
            channel.insert_one(message.dict())
            await connection.broadcast(json.dumps(message.json()))
    except WebSocketDisconnect:
        channel.disconnect(websocket)
