from typing import List
from datetime import datetime

from pydantic import BaseModel


class UserReviewSchema(BaseModel):
    review: str

    class Config:
        schema_extra = {
            "example": {
                "review": "Excelente, prepara un buen guiso de lentejas"
            }
        }


class UserReviewDB(UserReviewSchema):
    id: int
    reviewer: str
    reviewer_id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": 8,
                "review": "Excelente, prepara un buen guiso de lentejas",
                "reviewer": "Bob",
                "reviewer_id": 7,
                "createdAt": "2020-12-01T19:00:00.033Z",
                "updatedAt": "2020-12-01T19:00:00.033Z",
            }
        }


class UserReviewList(BaseModel):
    userId: int
    amount: int
    reviews: List[UserReviewDB]
