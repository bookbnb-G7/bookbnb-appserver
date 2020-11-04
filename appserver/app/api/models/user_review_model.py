from typing import List
from pydantic import BaseModel


class UserReviewSchema(BaseModel):
    review: str
    reviewer: str
    reviewer_id: str


class UserReviewDB(UserReviewSchema):
    id: int
    userId: int
    updatedAt: str
    createdAt: str


UserReviewList = List[UserReviewDB]
