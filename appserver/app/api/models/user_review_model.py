from typing import List, Optional
from pydantic import BaseModel


class UserReviewSchema(BaseModel):
    review: str
    reviewer: str
    reviewer_id: int


class UserReviewUpdate(BaseModel):
    review: Optional[str] = None
    reviewer: Optional[str] = None
    reviewer_id: Optional[int] = None


UserReviewList = List[UserReviewSchema]
