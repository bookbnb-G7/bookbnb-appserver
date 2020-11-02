from typing import List
from pydantic import BaseModel


class RoomRatingSchema(BaseModel):
    rating: int
    reviewer: str
    reviewer_id: int


class RoomRatingDB(RoomRatingSchema):
    id: int
    room_id: int


class RoomRatingList(BaseModel):
    room_id: int
    ratings: List[RoomRatingDB]
