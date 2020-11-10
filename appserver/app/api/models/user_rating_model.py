from typing import List
from pydantic import BaseModel


class UserRatingSchema(BaseModel):
    rating: int
    reviewer: str
    reviewer_id: int


UserRatingList = List[UserRatingSchema]
