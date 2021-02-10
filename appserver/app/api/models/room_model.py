from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class RoomSchema(BaseModel):
    title: str
    description: str
    type: str
    capacity: int
    latitude: float
    longitude: float
    location: str
    price_per_day: int

    class Config:
        schema_extra = {
            "example": {
                "title": "Exclusive offer in Las Toninas",
                "description": "Apartment with sights to the almighty beach",
                "type": "Apartment",
                "price_per_day": 67,
                "latitude": 0.0,
                "longitude": 0.0,
                "location": "USA",
                "capacity": 1,
            }
        }


class RoomDB(RoomSchema):
    id: int
    owner: str
    owner_uuid: int
    blocked: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": 2,
                "title": "Exclusive offer in Las Toninas",
                "description": "Apartment with sights to the almighty beach",
                "type": "Apartment",
                "owner": "Johnny",
                "owner_uuid": 45,
                "price_per_day": 67,
                "latitude": 0.0,
                "longitude": 0.0,
                "location": "USA",
                "capacity": 1,
                "blocked": False,
                "created_at": "2020-11-20T18:02:20.965Z",
                "updated_at": "2020-11-20T18:02:20.965Z",
            }
        }


class RoomUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    price_per_day: Optional[int] = None
    capacity: Optional[int] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        schema_extra = {"example": {"price_per_day": 456}}


class RoomList(BaseModel):
    amount: int
    rooms: List[RoomDB]

    class Config:
        schema_extra = {
            "example": {
                "amount": 2,
                "rooms": [
                    {
                        "id": 9,
                        "title": "Exclusive offer in Las Toninas",
                        "description": "Apartment with sights to the almighty beach",
                        "type": "Apartment",
                        "owner": "Alice",
                        "owner_uuid": 44,
                        "price_per_day": 67,
                        "latitude": 0.0,
                        "longitude": 0.0,
                        "location": "USA",
                        "capacity": 1,
                        "blocked": False,
                        "created_at": "2020-11-20T18:02:20.965Z",
                        "updated_at": "2020-11-20T18:02:20.965Z",
                    },
                    {
                        "id": 6,
                        "title": "House for 1 available",
                        "description": "Mansion-like house in springfield",
                        "type": "House",
                        "owner": "Bob",
                        "owner_uuid": 17,
                        "price_per_day": 872,
                        "latitude": 0.0,
                        "longitude": 0.0,
                        "location": "USA",
                        "capacity": 1,
                        "blocked": False,
                        "created_at": "2019-11-20T18:06:37.767Z",
                        "updated_at": "2020-11-20T18:06:37.767Z",
                    },
                ],
            }
        }
