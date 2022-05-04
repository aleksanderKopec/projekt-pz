import base64
import binascii
import os
from time import sleep

import pymongo
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from typing import Any, Dict, Union, List, Tuple

from pymongo.collection import Collection

from model.model import ChannelIdModel, MessageModel


def _validate_b64(s: str) -> bool:
    try:
        base64.b64decode(s, validate=True)
    except binascii.Error:
        return False
    return True


class DBManager:
    def __init__(self, mongo_url) -> None:
        self.db_client = pymongo.MongoClient(mongo_url)

        self.db = self.db_client["chat_db"]
        self.channels = self.db["channels"]

        # if there are no channels create one virtually
        if not list(self.channels.find()):
            self.channels.insert_one(ChannelIdModel(
                channel_no=0, channel_id="MAo=").dict())

    def get_channel_no(self, channel_id: str) -> int:
        if not _validate_b64(channel_id):
            raise Exception("Channel id has to be a valid base64 string.")

        channel = self.channels.find_one({"channel_id": channel_id})
        if channel is not None:
            channel_no = channel["channel_no"]
        else:
            channel_no = self.channels.find_one(
                sort=[("channel_no", pymongo.DESCENDING)])["channel_no"] + 1
            self.channels.insert_one(ChannelIdModel(
                channel_no=channel_no, channel_id=channel_id).dict())

        return channel_no

    def get_channel(self, channel_id: str) -> Collection:
        return self.db[f"channel_{self.get_channel_no(channel_id)}"]

    def get_messages(self, channel: Collection, number_of_messages: int = 0) -> list:
        messages = channel.find(
            sort=[("message_no", pymongo.DESCENDING)], limit=number_of_messages)
        return list(messages)

    def is_channel_empty(self, channel: Collection) -> bool:
        if not list(channel.find()):
            return False
        return True

    def get_next_message_no(self, channel: Collection) -> int:
        message = channel.find_one(sort=[("message_no", pymongo.DESCENDING)])
        if message is None:
            return 1
        return message["message_no"] + 1


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


class ChannelConnectionManager:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager
        self.channel_connections: Dict[int: ConnectionManager] = {}

    def get_channel_connection(self, channel_id: str) -> ConnectionManager:
        channel_no = self.db_manager.get_channel_no(channel_id)
        try:
            channel_connection = self.channel_connections[channel_no]
        except KeyError:
            channel_connection = ConnectionManager()
            self.channel_connections[channel_no] = channel_connection
        return channel_connection
