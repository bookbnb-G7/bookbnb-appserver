import os
import requests

from fastapi import APIRouter, UploadFile, File, Response, Depends
from firebase_admin import storage
from starlette.status import HTTP_200_OK

from app.api.crud.room_photo_dao import RoomPhotoDAO
from app.db import Session, get_db
from app.api.models.user_model import UserSchema
from app.api.models.room_photo_upload_model import RoomPhotoUploadResponse
from app.utils.image_utils import IdGenerator


USER_IMAGES_PATH = "users"
ROOM_IMAGES_PATH = "rooms"
USER_SERVER_API_URL = "https://bookbnb-userserver.herokuapp.com"
ROOM_SERVER_API_URL = "https://bookbnb-postserver.herokuapp.com"


router = APIRouter()


@router.post("/rooms/{room_id}/photos", response_model=RoomPhotoUploadResponse)
async def add_room_picture(
    room_id: int,
    response: Response,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    firebase_id = IdGenerator.generate()
    filename = f"{ROOM_IMAGES_PATH}/{room_id}/{firebase_id}"

    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_file(file.file)

    blob.make_public()
    image_url = blob.public_url

    new_photo_request = {"url": image_url, "firebase_id": firebase_id}
    photo_response = requests.post(
        f"{ROOM_SERVER_API_URL}/rooms/{room_id}/photos", json=new_photo_request
    )
    photo_id = photo_response.json()["id"]

    RoomPhotoDAO.add_new_room_photo(db, firebase_id, photo_id)
    response.status_code = photo_response.status_code
    return photo_response.json()


@router.patch(
    "/users/{user_id}/photo",
    response_model=UserSchema,
    status_code=HTTP_200_OK,
)
async def update_user_profile_picture(
    user_id: int, response: Response, file: UploadFile = File(...)
):
    _, image_extension = os.path.splitext(file.filename)
    filename = f"{USER_IMAGES_PATH}/{user_id}/profile{image_extension}"

    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_file(file.file)

    blob.make_public()
    image_url = blob.public_url

    user_patch = {"photo": image_url}
    user_response = requests.patch(
        f"{USER_SERVER_API_URL}/users/{user_id}", json=user_patch
    )
    response.status_code = user_response.status_code
    return user_response.json()
