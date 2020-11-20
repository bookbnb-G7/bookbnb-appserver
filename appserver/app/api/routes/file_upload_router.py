import os
import requests

from fastapi import APIRouter, UploadFile, File, Response
from firebase_admin import storage
from starlette.status import HTTP_200_OK

from app.api.models.user_model import UserSchema


USER_IMAGES_PATH = "users"
USER_SERVER_API_URL = "https://bookbnb-userserver.herokuapp.com"


router = APIRouter()

"""@router.post("/upload_room_pictures", response_model=RoomDB, status_code=HTTP_200_OK)
async def update_room_pictures(
    file: List[UploadFile] = File(...), user_id: int = Form(...)
):
    for image in file:
        _, image_extension = os.path.splitext(image.filename)
        filename = f"{USER_IMAGES_PATH}/{user_id}/profile{image_extension}"

        bucket = storage.bucket()

        blob = bucket.blob(filename)
        blob.upload_from_file(image.file)

        blob.make_public()
        image_url = blob.public_url

        user_patch = {"photo": image_url}

    return requests.patch(f"{USER_SERVER_API_URL}/users/{user_id}", json=user_patch)"""


@router.post(
    "/upload_profile_picture/{user_id}",
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
