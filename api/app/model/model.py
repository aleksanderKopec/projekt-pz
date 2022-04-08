import datetime
from typing import List

from pydantic import BaseModel


class MessageModel(BaseModel):
    message_id: int
    author: str
    message: str
    timestamp: datetime.datetime


class ChannelModel(BaseModel):
    channel_id: str
    messages: List[MessageModel]


class ChannelIdModel(BaseModel):
    channel_no: int
    channel_id: str
