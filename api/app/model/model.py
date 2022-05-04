from typing import List

from pydantic import BaseModel


class MessageModel(BaseModel):
    message_no: int
    author: str
    message: str
    timestamp: str  # datetime.datetime.isoformat('2022-04-18T18:53:22.831797')
    is_encrypted: bool

    class Config:
        schema_extra = {
            "example": {
                "message_no": 1,
                "author": "Jane Doe",
                "message": "Hi!",
                "timestamp": "2022-04-18T18:53:22.831797",
                "is_encrypted": False
            }
        }


class MessagesModel(BaseModel):
    channel_id: str
    messages: List[MessageModel]

    class Config:
        schema_extra = {
            "example": {
                "channel_id": "dGVzdAo=",
                "messages": [
                    {
                        "message_no": 1,
                        "author": "Jane Doe",
                        "message": "Hi!",
                        "timestamp": "2022-04-18T18:53:22.831797",
                        "is_encrypted": False
                    },
                    {
                        "message_no": 2,
                        "author": "John Smith",
                        "message": "Hello!",
                        "timestamp": "2022-04-18T18:54:32.832345",
                        "is_encrypted": False
                    }
                ]
            }
        }


class ChannelIdModel(BaseModel):
    channel_no: int
    channel_id: str

    class Config:
        schema_extra = {
            "example": {
                "channel_no": 1,
                "channel_id": "dGVzdAo="
            }
        }
