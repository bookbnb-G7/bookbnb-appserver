import logging

from app.errors.http_error import NotFoundError
from app.model.room_photo import RoomPhoto

logger = logging.getLogger(__name__)


class RoomPhotoDAO:
    @classmethod
    def add_new_room_photo(cls, db, firebase_id, room_photo_id):
        new_room_photo = RoomPhoto(firebase_id=firebase_id, room_photo_id=room_photo_id)

        db.add(new_room_photo)
        db.commit()

        logger.info("New room photo added")
        logger.debug(
            "Details of the new photo, firebase_id: %s, photo_id: %s",
            firebase_id,
            room_photo_id,
        )

        return new_room_photo.serialize()

    @classmethod
    def get_room_photo(cls, db, firebase_id):
        room_photo = (
            db.query(RoomPhoto).filter(RoomPhoto.firebase_id == firebase_id).first()
        )

        if room_photo is None:
            logger.warning("Photo with firebase id: %s not found", firebase_id)
            return None

        return room_photo.serialize()

    @classmethod
    def delete_room_photo(cls, db, firebase_id):
        room_photo = (
            db.query(RoomPhoto).filter(RoomPhoto.firebase_id == firebase_id).first()
        )

        if room_photo is None:
            logger.debug("Firebase id of the not found photo: %s", firebase_id)
            raise NotFoundError("Room photo")

        db.delete(room_photo)
        db.commit()

        logger.info("Room photo added")
        logger.debug("Firebase id of the deleted photo: %s", firebase_id)

        return room_photo.serialize()
