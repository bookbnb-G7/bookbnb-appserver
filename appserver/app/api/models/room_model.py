from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class RoomSchema(BaseModel):
    type: str
    owner: str
    owner_id: int
    price_per_day: float

    class Config:
        schema_extra = {
            "example": {
                "type": "Apartment",
                "owner": "Johnny",
                "owner_id": 45,
                "price_per_day": 67,
            }
        }


class RoomUpdate(BaseModel):
    type: Optional[str] = None
    price_per_day: Optional[float] = None

    class Config:
        schema_extra = {"example": {"price_per_day": 456}}


class RoomDB(RoomSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "type": "Apartment",
                "owner": "Johnny",
                "owner_id": 45,
                "price_per_day": 67,
                "id": 2,
                "created_at": "2020-11-20T18:02:20.965Z",
                "updated_at": "2020-11-20T18:02:20.965Z",
            }
        }


class RoomList(BaseModel):
    amount: int
    rooms: List[RoomDB]

    class Config:
        schema_extra = {
            "example": {
                "amount": 0,
                "rooms": [
                    {
                        "type": "Apartment",
                        "owner": "Alice",
                        "owner_id": 44,
                        "price_per_day": 67,
                        "id": 9,
                        "created_at": "2020-11-20T18:02:20.965Z",
                        "updated_at": "2020-11-20T18:02:20.965Z",
                    },
                    {
                        "type": "House",
                        "owner": "Bob",
                        "owner_id": 17,
                        "price_per_day": 872,
                        "id": 6,
                        "created_at": "2019-11-20T18:06:37.767Z",
                        "updated_at": "2020-11-20T18:06:37.767Z",
                    },
                ],
            }
        }
