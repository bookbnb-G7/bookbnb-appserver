import os

from app.api.crud.room_photo_dao import RoomPhotoDAO
from app.api.models.room_photo_model import RoomPhoto, RoomPhotoList
from app.api.models.user_model import UserSchema
from app.db import get_db
from app.dependencies import check_token, get_uuid_from_xtoken
from app.errors.http_error import NotFoundError, UnauthorizedRequestError
from app.services.authsender import AuthSender
from app.services.requester import Requester
from app.utils.image_utils import IdGenerator
from fastapi import APIRouter, Depends, File, Response, UploadFile
from firebase_admin import storage
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

USER_IMAGES_PATH = "users"
ROOM_IMAGES_PATH = "rooms"
USER_SERVER_API_URL = os.environ["USERSERVER_URL"]
ROOM_SERVER_API_URL = os.environ["POSTSERVER_URL"]


router = APIRouter()


@router.post(
    "/rooms/{room_id}/photos",
    response_model=RoomPhoto,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def add_room_picture(
    room_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    uuid: int = Depends(get_uuid_from_xtoken),
):
    room_path = f"/rooms/{room_id}"
    room, _ = Requester.room_srv_fetch("GET", room_path, {HTTP_200_OK})

    if not AuthSender.has_permission_to_modify(room["owner_uuid"], uuid):
        raise UnauthorizedRequestError("You can't add photos to another user room!")

    firebase_id = IdGenerator.generate()
    filename = f"{ROOM_IMAGES_PATH}/{room_id}/{firebase_id}"

    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_file(file.file)
    blob.make_public()
    image_url = blob.public_url

    room_photo_path = f"/rooms/{room_id}/photos"
    new_photo_request = {"url": image_url, "firebase_id": firebase_id}
    photo_response, _ = Requester.room_srv_fetch(
        "POST", room_photo_path, {HTTP_201_CREATED}, payload=new_photo_request
    )
    photo_id = photo_response["id"]

    RoomPhotoDAO.add_new_room_photo(db, firebase_id, photo_id)
    return photo_response


@router.get(
    "/rooms/{room_id}/photos", response_model=RoomPhotoList, status_code=HTTP_200_OK
)
async def get_all_room_photos(
    room_id: int,
):
    room_photo_path = f"/rooms/{room_id}/photos"
    photo_response, _ = Requester.room_srv_fetch("GET", room_photo_path, {HTTP_200_OK})
    return photo_response


@router.get(
    "/rooms/{room_id}/photos/{firebase_id}",
    response_model=RoomPhoto,
    status_code=HTTP_200_OK,
)
async def get_room_photo(
    room_id: int,
    firebase_id: int,
    db: Session = Depends(get_db),
):
    photo = RoomPhotoDAO.get_room_photo(db, firebase_id)

    photo_id = photo["room_photo_id"]
    room_photo_path = f"/rooms/{room_id}/photos/{photo_id}"

    photo_response, _ = Requester.room_srv_fetch("GET", room_photo_path, {HTTP_200_OK})
    return photo_response


@router.delete(
    "/rooms/{room_id}/photos/{firebase_id}",
    response_model=RoomPhoto,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_room_photo(
    room_id: int,
    firebase_id: int,
    db: Session = Depends(get_db),
    uuid: int = Depends(get_uuid_from_xtoken),
):
    room_path = f"/rooms/{room_id}"
    room, _ = Requester.room_srv_fetch("GET", room_path, {HTTP_200_OK})

    if not AuthSender.has_permission_to_modify(room["owner_uuid"], uuid):
        raise UnauthorizedRequestError("You can't delete photos of another user room!")

    blob_name = f"{ROOM_IMAGES_PATH}/{room_id}/{firebase_id}"
    bucket = storage.bucket()
    blob = bucket.get_blob(blob_name)
    if blob is None:
        raise NotFoundError("Photo")
    blob.delete()

    photo = RoomPhotoDAO.delete_room_photo(db, firebase_id)
    if photo is None:
        raise NotFoundError("Photo id")
    photo_id = photo["room_photo_id"]

    room_photo_path = f"/rooms/{room_id}/photos/{photo_id}"
    photo_response, _ = Requester.room_srv_fetch(
        "DELETE", room_photo_path, {HTTP_200_OK}
    )
    return photo_response


@router.patch(
    "/users/{user_id}/photo",
    response_model=UserSchema,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def update_user_profile_picture(
    user_id: int,
    response: Response,
    file: UploadFile = File(...),
    uuid: int = Depends(get_uuid_from_xtoken),
):
    if not AuthSender.has_permission_to_modify(user_id, uuid):
        raise UnauthorizedRequestError("You can't modify the photo of another user!")
    _, image_extension = os.path.splitext(file.filename)
    filename = f"{USER_IMAGES_PATH}/{user_id}/profile{image_extension}"

    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_file(file.file)

    blob.make_public()
    image_url = blob.public_url

    user_patch = {"photo": image_url}
    user_profile_path = f"/users/{user_id}"
    user_response, _ = Requester.user_srv_fetch(
        "PATCH", user_profile_path, {HTTP_200_OK}, payload=user_patch
    )
    return user_response
