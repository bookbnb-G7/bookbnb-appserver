from datetime import datetime
from typing import List

from pydantic import BaseModel


class RoomBookingSchema(BaseModel):
    date_ends: datetime
    date_begins: datetime
    amount_of_people: int


class RoomBookingDB(RoomBookingSchema):
    id: int
    user_id: int
    room_id: int
    total_price: float
    created_at: datetime
    updated_at: datetime


class RoomBookingList(BaseModel):
    amount: int
    room_id: int
    bookings: List[RoomBookingDB]


class UserBooking(BaseModel):
    booking_id: int
    room_id: int


class UserBookingList(BaseModel):
    userId: int
    amount: int
    roomBookings: List[UserBooking]
