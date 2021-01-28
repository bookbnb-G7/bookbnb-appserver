from typing import List, Optional

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

    class Config:
        schema_extra = {
            "example": {
                "id": 2,
                "rating": 5,
                "reviewer": "Bob",
                "reviewer_id": 17,
            }
        }


class UserRatingList(BaseModel):
    userId: int
    amount: int
    ratings: List[UserRatingDB]
