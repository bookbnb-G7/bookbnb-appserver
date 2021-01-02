from datetime import date, datetime
from typing import List

from pydantic import BaseModel


class RoomBookingSchema(BaseModel):
    date_ends: date
    date_begins: date
    amount_of_people: int
    user_id: int


class RoomBookingDB(RoomBookingSchema):
    id: int
    room_id: int
    total_price: float
    status: int
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
