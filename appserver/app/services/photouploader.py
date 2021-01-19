import os

import firebase_admin
from app.config import firebase_credentials, logger
from app.errors.http_error import NotFoundError
from app.utils.image_utils import IdGenerator
from firebase_admin import storage


class PhotoUploader:
    ROOM_IMAGES_PATH = "rooms"
    USER_IMAGES_PATH = "users"

    def __init__(self, credentials):
        storage_bucket = os.environ.get("FIREBASE_STORAGE_BUCKET")

        self.app = firebase_admin.initialize_app(
            credentials, {"storageBucket": storage_bucket}, name="bookbnb-photouploader"
        )

        logger.info("Authenticated in firebase successfully")

    def upload_profile_photo(self, file, uuid):
        _, image_extension = os.path.splitext(file.filename)
        filename = f"{self.USER_IMAGES_PATH}/{uuid}/profile{image_extension}"

        image_url = self._upload_image(file, filename)

        return image_url

    def upload_room_photo(self, file, room_id):
        img_firebase_id = IdGenerator.generate()
        filename = f"{self.ROOM_IMAGES_PATH}/{room_id}/{img_firebase_id}"

        image_url = self._upload_image(file, filename)

        return image_url, img_firebase_id

    def remove_room_photo(self, room_id, img_firebase_id):
        filename = f"{self.ROOM_IMAGES_PATH}/{room_id}/{img_firebase_id}"
        self._remove_image(filename)

    @staticmethod
    def _upload_image(file, filename):
        bucket = storage.bucket()
        blob = bucket.blob(filename)
        blob.upload_from_file(file.file)
        blob.make_public()

        return blob.public_url

    @staticmethod
    def _remove_image(filename):
        bucket = storage.bucket()
        blob = bucket.get_blob(filename)
        if blob is None:
            raise NotFoundError("Photo")

        blob.delete()


class PhotoUploaderFake:
    def upload_profile_photo(self, file, uuid):
        return

    def upload_room_photo(self, file, room_id):
        return

    def remove_room_photo(self, room_id, img_firebase_id):
        return


photouploader = None
if os.environ.get("ENVIRONMENT") == "production":
    photouploader = PhotoUploader(firebase_credentials)
else:
    photouploader = PhotoUploaderFake()
