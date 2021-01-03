from datetime import date
from typing import List

from pydantic import BaseModel

# TODO: Change file name to booking_model.py


class BookingSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingDB(BookingSchema):
    id: int
    price: int
    booker_id: int
    room_owner_id: int
    booking_status: int
    transaction_hash: str
    transaction_status: int


class BookingList(BaseModel):
    amount: int
    bookings: List[BookingDB]


class BookingsUserList(BaseModel):
    made: BookingList
    received: BookingList
