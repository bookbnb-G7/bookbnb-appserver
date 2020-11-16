from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class RoomReviewSchema(BaseModel):
    review: str
    reviewer: str
    reviewer_id: int


class RoomReviewUpdate(BaseModel):
    review: Optional[str] = None


class RoomReviewDB(RoomReviewSchema):
    id: int
    room_id: int
    created_at: datetime
    updated_at: datetime


class RoomReviewList(BaseModel):
    amount: int
    room_id: int
    reviews: List[RoomReviewDB]
