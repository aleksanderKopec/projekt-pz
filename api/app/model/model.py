import datetime
from typing import List

from pydantic import BaseModel


class Message(BaseModel):
    author: str
    message: str
    timestamp: datetime.datetime


class ChatRoom(BaseModel):
    room_id: str
    messages: List[Message]

