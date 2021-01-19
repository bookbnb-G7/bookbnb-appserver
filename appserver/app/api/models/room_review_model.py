from datetime import datetime
from typing import List

from pydantic import BaseModel


class RoomReviewSchema(BaseModel):
    review: str

    class Config:
        schema_extra = {
            "example": {
                "review": "Excelente, prepara un buen guiso de lentejas",
            }
        }


class RoomReviewDB(RoomReviewSchema):
    id: int
    room_id: int
    reviewer: str
    reviewer_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "review": "Muy lindo todo",
                "reviewer": "Bob",
                "reviewer_id": 198,
                "id": 2,
                "room_id": 9,
                "created_at": "2020-11-20T18:13:31.378Z",
                "updated_at": "2020-11-20T18:13:31.378Z",
            }
        }


class RoomReviewList(BaseModel):
    amount: int
    room_id: int
    reviews: List[RoomReviewDB]

    class Config:
        schema_extra = {
            "example": {
                "amount": 0,
                "room_id": 0,
                "reviews": [
                    {
                        "review": "Jag gillade lägenheten",
                        "reviewer": "Alice",
                        "reviewer_id": 34,
                        "id": 90,
                        "room_id": 6,
                        "created_at": "2020-11-20T18:19:11.706Z",
                        "updated_at": "2020-11-20T18:19:11.706Z",
                    },
                    {
                        "review": "Very good",
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
