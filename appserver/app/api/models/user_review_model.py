from typing import List, Optional

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

    class Config:
        schema_extra = {
            "example": {
                "id": 8,
                "review": "Excelente, prepara un buen guiso de lentejas",
                "reviewer": "Bob",
                "reviewer_id": 7,
            }
        }


class UserReviewList(BaseModel):
    userId: int
    amount: int
    reviews: List[UserReviewDB]
