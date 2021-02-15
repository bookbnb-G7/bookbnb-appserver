from pydantic import BaseModel


class UserFavoriteRoomSchema(BaseModel):
    room_id: int

    class Config:
        schema_extra = {
            "example": {
                "room_id": 5
            }
        }
