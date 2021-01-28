from typing import List
from datetime import datetime

from pydantic import BaseModel


class UserRatingSchema(BaseModel):
    rating: int

    class Config:
        schema_extra = {
            "example": {
                "rating": 5,
            }
        }


class UserRatingDB(UserRatingSchema):
    id: int
    reviewer: str
    reviewer_id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": 2,
                "rating": 5,
                "reviewer": "Bob",
                "reviewer_id": 17,
                "createdAt": "2020-12-01T19:00:00.033Z",
                "updatedAt": "2020-12-01T19:00:00.033Z",
            }
        }


class UserRatingList(BaseModel):
    userId: int
    amount: int
    ratings: List[UserRatingDB]
