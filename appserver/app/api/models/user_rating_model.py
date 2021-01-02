from typing import List, Optional

from pydantic import BaseModel


class UserRatingSchema(BaseModel):
    rating: int
    reviewer: str
    reviewer_id: int

    class Config:
        schema_extra = {
            "example": {
                "rating": 5,
                "reviewer": "Bob",
                "reviewer_id": 17,
            }
        }


class UserRatingUpdate(BaseModel):
    rating: Optional[int] = None
    reviewer: Optional[str] = None
    reviewer_id: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "rating": 4,
            }
        }


class UserRatingList(BaseModel):
    userId: int
    amount: int
    ratings: List[UserRatingSchema]
