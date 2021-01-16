from typing import List
from pydantic import BaseModel


class MessageSchema(BaseModel):
    receiver_uuid: int
    message: str


class MessageDB(MessageSchema):
    sender_name: str
    receiver_name: str
    sender_uuid: int
    timestamp: int


class ChatPreview(BaseModel):
    other_user: str
    other_uuid: int
    last_message: str


class ChatDB(ChatPreview):
    amount: int
    messages: List[MessageDB]


class ChatList(BaseModel):
    amount: int
    chats: List[ChatPreview]
