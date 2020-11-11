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
    created_at: str
    updated_at: str


class RoomRatingList(BaseModel):
    room_id: int
    ratings: List[RoomRatingDB]
