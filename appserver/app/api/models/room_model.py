from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class RoomSchema(BaseModel):
    type: str
    price_per_day: int

    class Config:
        schema_extra = {
            "example": {
                "type": "Apartment",
                "price_per_day": 67,
            }
        }


class RoomDB(RoomSchema):
    id: int
    owner: str
    owner_uuid: int
    created_at: datetime
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": 2,
                "type": "Apartment",
                "owner": "Johnny",
                "owner_uuid": 45,
                "price_per_day": 67,
                "created_at": "2020-11-20T18:02:20.965Z",
                "updated_at": "2020-11-20T18:02:20.965Z",
            }
        }


class RoomUpdate(BaseModel):
    type: Optional[str] = None
    price_per_day: Optional[int] = None

    class Config:
        schema_extra = {"example": {"price_per_day": 456}}


class RoomList(BaseModel):
    amount: int
    rooms: List[RoomDB]

    class Config:
        schema_extra = {
            "example": {
                "amount": 0,
                "rooms": [
                    {
                        "id": 9,
                        "type": "Apartment",
                        "owner": "Alice",
                        "owner_id": 44,
                        "price_per_day": 67,
                        "created_at": "2020-11-20T18:02:20.965Z",
                        "updated_at": "2020-11-20T18:02:20.965Z",
                    },
                    {
                        "id": 6,
                        "type": "House",
                        "owner": "Bob",
                        "owner_id": 17,
                        "price_per_day": 872,
                        "created_at": "2019-11-20T18:06:37.767Z",
                        "updated_at": "2020-11-20T18:06:37.767Z",
                    },
                ],
            }
        }
