from datetime import datetime
from pydantic import BaseModel


class RoomPhotoUploadResponse(BaseModel):
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
