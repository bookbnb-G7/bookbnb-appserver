from sqlalchemy import Column, Integer

from app.db import Base


class RoomPhoto(Base):

    __tablename__ = "room_photos"

    id = Column("id", Integer, primary_key=True)
    firebase_id = Column(Integer, nullable=False)
    room_photo_id = Column(Integer, nullable=False)

    def __init__(self, firebase_id, room_photo_id):
        self.firebase_id = firebase_id
        self.room_photo_id = room_photo_id

    def serialize(self):
        return {
            "id": self.id,
            "firebase_id": self.firebase_id,
            "room_photo_id": self.room_photo_id,
        }
