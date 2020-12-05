from datetime import datetime
from typing import List

from pydantic import BaseModel


class RoomPhoto(BaseModel):
    url: str
    firebase_id: int
    id: int
    room_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "url": "www.google.com",
                "firebase_id": 2,
                "id": 4,
                "room_id": 8,
                "created_at": "2020-12-01T19:00:00.033Z",
                "updated_at": "2020-12-01T19:00:00.033Z",
            }
        }


class RoomPhotoList(BaseModel):
    amount: int
    room_id: int
    room_photos: List[RoomPhoto]

    class Config:
        schema_extra = {
            "example": {
                "amount": 2,
                "room_id": 3,
                "room_photos": [
                    {
                        "url": "www.google.com",
                        "firebase_id": 8,
                        "id": 4,
                        "room_id": 3,
                        "created_at": "2020-12-01T19:00:00.033Z",
                        "updated_at": "2020-12-01T19:00:00.033Z",
                    },
                    {
                        "url": "www.yaaaaaaaaaaaa.com",
                        "firebase_id": 9,
                        "id": 5,
                        "room_id": 3,
                        "created_at": "2020-12-01T19:00:00.033Z",
                        "updated_at": "2020-12-01T19:00:00.033Z",
                    },
                ],
            }
        }
