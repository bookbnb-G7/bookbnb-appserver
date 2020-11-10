from typing import List
from pydantic import BaseModel


class UserReviewSchema(BaseModel):
    review: str
    reviewer: str
    reviewer_id: int


UserReviewList = List[UserReviewSchema]
