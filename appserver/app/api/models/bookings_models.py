from datetime import date, datetime
from typing import List

from pydantic import BaseModel


class BookingSchema(BaseModel):
    roomId: int
    date_from: date
    date_to: date


class BookingDB(BookingSchema):
    id: int
    price: int
    room_id: int
    bookerId: int
    room_owner_id: int
    date_from: date
    date_to: date
    booking_status: int
    transaction_hash: str
    transaction_status: int

    created_at: datetime
    updated_at: datetime


class BookingList(BaseModel):
    amount: int
    room_id: int
    bookings: List[BookingDB]
