from typing import Optional

from pydantic import BaseModel


class RoomSchema(BaseModel):
    type: str
    owner: str
    owner_id: int
    price_per_day: float


class RoomUpdate(BaseModel):
    type: Optional[str] = None
    price_per_day: Optional[float] = None


class RoomDB(RoomSchema):
    id: int
    created_at: str
    updated_at: str
