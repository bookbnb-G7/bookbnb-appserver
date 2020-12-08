from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class RoomRatingSchema(BaseModel):
    rating: int

    class Config:
        schema_extra = {
            "example": {
                "rating": 4,
            }
        }


class RoomRatingUpdate(BaseModel):
    rating: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "rating": 5,
            }
        }


class RoomRatingDB(RoomRatingSchema):
    id: int
    room_id: int
    reviewer: str
    reviewer_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": 5,
                "rating": 4,
                "reviewer": "Bob",
                "reviewer_id": 17,
                "room_id": 8,
                "created_at": "2020-11-20T18:13:31.378Z",
                "updated_at": "2020-11-20T18:13:31.378Z",
            }
        }


class RoomRatingList(BaseModel):
    amount: int
    room_id: int
    ratings: List[RoomRatingDB]

    class Config:
        schema_extra = {
            "example": {
                "amount": 0,
                "room_id": 0,
                "ratings": [
                    {
                        "rating": 3,
                        "reviewer": "Alice",
                        "reviewer_id": 34,
                        "id": 90,
                        "room_id": 6,
                        "created_at": "2020-11-20T18:19:11.706Z",
                        "updated_at": "2020-11-20T18:19:11.706Z",
                    },
                    {
                        "rating": 2,
                        "reviewer": "Bob",
                        "reviewer_id": 24,
                        "id": 98,
                        "room_id": 6,
                        "created_at": "2020-11-20T18:19:11.706Z",
                        "updated_at": "2020-11-20T18:19:11.706Z",
                    },
                ],
            }
        }
