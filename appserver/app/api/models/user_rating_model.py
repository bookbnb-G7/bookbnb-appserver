from typing import List, Optional
from pydantic import BaseModel


class UserRatingSchema(BaseModel):
    rating: int
    reviewer: str
    reviewer_id: int


class UserRatingUpdate(BaseModel):
    rating: Optional[int] = None
    reviewer: Optional[str] = None
    reviewer_id: Optional[int] = None


UserRatingList = List[UserRatingSchema]
