import base64
import binascii
import os
from time import sleep

import pymongo
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from typing import Any, Dict, Union, List, Tuple

from pymongo.collection import Collection


class DBManager:
    def __init__(self, mongo_url):
        self.db_client = pymongo.MongoClient(mongo_url)

        self.db = self.db_client["chat_db"]
        self.channel_id_db = self.db["channel_id"]

        self.db["room_0"]
        self.channel_id_db.insert_one({"channel_id": "0", "channel_no": 0})

    async def get_channel(self, channel_id: str):
        # validate base64
        try:
            base64.b64decode(channel_id)
        except binascii.Error:
            raise HTTPException(
                status_code=500, detail=f"Channel ID not b64 encoded")

        channel_id_no = self.channel_id_db.find_one({"channel_id": channel_id})
        if channel_id_no is None:
            channel_no = self.channel_id_db.find_one(
                sort=[("channel_id", pymongo.DESCENDING)])["channel_no"] + 1
            channel_id_no = {"channel_id": channel_id,
                             "channel_no": channel_no}
            self.channel_id_db.insert_one(channel_id_no)

        channel_no = channel_id_no["channel_no"]
        channel = self.db[f"room_{channel_no}"]
        print(channel_no)
        return (channel, channel_no)

    async def get_last_message_no(self, channel_no):
        last_msg = self.db[f"room_{channel_no}"].find_one(sort=[("message_id", pymongo.DESCENDING)])
        if last_msg is None:
            last_msg = 0
        else:
            last_msg = last_msg["message_id"]
        return last_msg


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


class ChannelManager:
    def __init__(self, db):
        self.db = db
        self.channels: Dict[int: ConnectionManager] = {}

    def _open_channel(self, channel_no):
        channel = ConnectionManager()
        self.channels[channel_no] = channel
        return channel

    def get_channel(self, channel_no):
        try:
            channel = self.channels[channel_no]
        except KeyError:
            channel = self._open_channel(channel_no)
        return channel
