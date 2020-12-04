from app.model.room_photo import RoomPhoto
from app.errors.http_error import NotFoundError


class RoomPhotoDAO:
    @classmethod
    def add_new_room_photo(cls, db, firebase_id, room_photo_id):
        new_room_photo = RoomPhoto(firebase_id=firebase_id, room_photo_id=room_photo_id)

        db.add(new_room_photo)
        db.commit()

        return new_room_photo.serialize()

    @classmethod
    def get_room_photo(cls, db, firebase_id):
        room_photo = (
            db.query(RoomPhoto).where(firebase_id=RoomPhoto.firebase_id).first()
        )

        if room_photo is None:
            return None

        return room_photo.serialize()

    @classmethod
    def delete_room_photo(cls, db, firebase_id):
        room_photo = (
            db.query(RoomPhoto).where(firebase_id=RoomPhoto.firebase_id).first()
        )

        if room_photo is None:
            raise NotFoundError("room")

        db.delete(room_photo)
        db.commit()

        return room_photo.serialize()
