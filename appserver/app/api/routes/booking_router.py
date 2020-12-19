import json
import logging

from app.api.models.bookings_models import (RoomBookingDB, RoomBookingList,
                                            RoomBookingSchema, UserBooking,
                                            UserBookingList)
from app.dependencies import check_token, get_uuid_from_xtoken
from app.errors.http_error import (NotAllowedRequestError,
                                   UnauthorizedRequestError)
from app.errors.utils import get_error_message
from app.services.authsender import AuthSender
from app.services.requester import Requester
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/rooms/{room_id}/bookings", response_model=RoomBookingList, status_code=HTTP_200_OK
)
async def get_all_room_bookings(room_id: int):
    path = f"/rooms/{room_id}/bookings"
    bookings, status_code = Requester.room_srv_fetch("GET", path)
    if status_code != HTTP_200_OK:
        raise HTTPException(status_code=status_code, detail=get_error_message(bookings))

    return bookings


@router.post(
    "/rooms/{room_id}/bookings",
    response_model=RoomBookingDB,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def add_booking_to_room(
    room_id: int,
    payload: RoomBookingSchema,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    room_path = f"/rooms/{room_id}"
    room, status_code = Requester.room_srv_fetch("GET", room_path)

    if status_code != HTTP_200_OK:
        raise HTTPException(status_code=status_code, detail=get_error_message(room))

    if not AuthSender.can_book_room(room["owner_uuid"], uuid):
        raise NotAllowedRequestError("Can't create booking of your own room")

    booking_path = f"/rooms/{room_id}/bookings"
    payload_booking = payload.dict()
    payload_booking.update({"user_id": uuid})
    serialized_booking_payload = json.dumps(payload_booking, default=str)
    booking, status_code = Requester.room_srv_fetch(
        "POST", booking_path, serialized_booking_payload
    )

    if status_code != HTTP_201_CREATED:
        raise HTTPException(status_code=status_code, detail=get_error_message(booking))

    user_path = f"/users/{uuid}/bookings"
    booking_id = booking["id"]
    user_booking_payload = {"booking_id": booking_id, "room_id": room_id}
    user_booking, status_code = Requester.user_srv_fetch(
        "POST", user_path, user_booking_payload
    )

    if status_code != HTTP_201_CREATED:
        raise HTTPException(
            status_code=status_code, detail=user_booking.json()["detail"]
        )

    return booking


@router.get(
    "/rooms/{room_id}/bookings/{booking_id}",
    response_model=RoomBookingDB,
    status_code=HTTP_200_OK,
)
async def get_room_booking(room_id: int, booking_id: int):
    path = f"/rooms/{room_id}/bookings/{booking_id}"
    booking, status_code = Requester.room_srv_fetch("GET", path)

    if status_code != HTTP_200_OK:
        raise HTTPException(status_code=status_code, detail=get_error_message(booking))

    return booking


@router.delete(
    "/rooms/{room_id}/bookings/{booking_id}",
    response_model=RoomBookingDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_room_booking(
    room_id: int, booking_id: int, uuid: int = Depends(get_uuid_from_xtoken)
):
    booking_path = f"/rooms/{room_id}/bookings/{booking_id}"
    booking, status_code = Requester.room_srv_fetch("GET", booking_path)

    if status_code != HTTP_200_OK:
        raise HTTPException(status_code=status_code, detail=get_error_message(booking))

    if not AuthSender.has_permission_to_modify(uuid, booking["user_id"]):
        raise UnauthorizedRequestError("Can't delete other users bookings")

    booking, status_code = Requester.room_srv_fetch("DELETE", booking_path)
    if status_code != HTTP_200_OK:
        raise HTTPException(status_code=status_code, detail=get_error_message(booking))

    user_path = f"/users/{uuid}/bookings/{booking_id}"
    user_booking, status_code = Requester.user_srv_fetch("DELETE", user_path)
    if status_code != HTTP_200_OK:
        raise HTTPException(
            status_code=status_code, detail=get_error_message(user_booking)
        )

    return booking


@router.get(
    "/users/{room_id}/bookings/{booking_id}",
    response_model=UserBooking,
    status_code=HTTP_200_OK,
)
async def get_user_booking(room_id: int, booking_id: int):
    path = f"/users/{room_id}/bookings/{booking_id}"
    booking, status_code = Requester.user_srv_fetch("GET", path)

    if status_code != HTTP_200_OK:
        raise HTTPException(status_code=status_code, detail=get_error_message(booking))

    return booking


@router.get(
    "/users/{room_id}/bookings", response_model=UserBookingList, status_code=HTTP_200_OK
)
async def get_all_user_bookings(room_id: int):
    path = f"/users/{room_id}/bookings"
    bookings, status_code = Requester.user_srv_fetch("GET", path)
    if status_code != HTTP_200_OK:
        raise HTTPException(status_code=status_code, detail=get_error_message(bookings))

    return bookings
