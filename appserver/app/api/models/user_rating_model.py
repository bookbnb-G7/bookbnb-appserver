from typing import List
from pydantic import BaseModel


class UserRatingSchema(BaseModel):
    rating: int
    reviewer: str
    reviewer_id: str


class UserRatingDB(UserRatingSchema):
    id: int
    userId: int
    updatedAt: str
    createdAt: str


UserRatingList = List[UserRatingDB]
