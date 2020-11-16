from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class RoomRatingSchema(BaseModel):
    rating: int
    reviewer: str
    reviewer_id: int


class RoomRatingUpdate(BaseModel):
    rating: Optional[int] = None


class RoomRatingDB(RoomRatingSchema):
    id: int
    room_id: int
    created_at: datetime
    updated_at: datetime


class RoomRatingList(BaseModel):
    amount: int
    room_id: int
    ratings: List[RoomRatingDB]
