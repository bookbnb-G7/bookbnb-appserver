import json
import logging
import datetime

from app.api.models.bookings_models import (RoomBookingDB, RoomBookingList,
                                            RoomBookingSchema, UserBooking,
                                            UserBookingList)
from app.dependencies import check_token, get_uuid_from_xtoken
from app.errors.http_error import (NotAllowedRequestError,
                                   UnauthorizedRequestError)
from app.services.authsender import AuthSender
from app.services.requester import Requester
from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/rooms/{room_id}/bookings", response_model=RoomBookingList, status_code=HTTP_200_OK
)
async def get_all_room_bookings(room_id: int):
    path = f"/rooms/{room_id}/bookings"
    bookings, _ = Requester.room_srv_fetch("GET", path, {HTTP_200_OK})

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
    room, _ = Requester.room_srv_fetch("GET", room_path, {HTTP_200_OK})

    if not AuthSender.can_book_room(room["owner_uuid"], uuid):
        raise NotAllowedRequestError("Can't create booking of your own room")

    # Create intent book in payment server

    booking_path = "/bookings"
    payload_booking = payload.dict()
    payload_booking = {
        "bookerId": payload.user_id,
        "roomId": room_id,
        "dateFrom": payload.date_begins.strftime('%d-%m-%Y'),
        "dateTo": payload.date_ends.strftime('%d-%m-%Y')
    }
    booking, _ = Requester.payment_fetch(
        method="POST",
        path=booking_path,
        expected_statuses={HTTP_201_CREATED},
        payload=payload_booking
    )

    # Create booking in room server

    booking_path = f"/rooms/{room_id}/bookings"
    payload_booking = payload.dict()
    payload_booking.update({"user_id": uuid})
    # Add the booking id and status received from the payment server
    payload_booking["id"] = booking["id"]
    payload_booking["status"] = booking["bookingStatus"]
    serialized_booking_payload = json.dumps(payload_booking, default=str)
    booking, _ = Requester.room_srv_fetch(
        "POST", booking_path, {HTTP_201_CREATED}, payload=serialized_booking_payload
    )

    user_path = f"/users/{uuid}/bookings"
    booking_id = booking["id"]
    user_booking_payload = {"booking_id": booking_id, "room_id": room_id}
    Requester.user_srv_fetch(
        "POST", user_path, {HTTP_201_CREATED}, payload=user_booking_payload
    )

    return booking


@router.post(
    "/rooms/{room_id}/bookings/{booking_id}/accept",
    response_model=RoomBookingDB,
    status_code=HTTP_200_OK,
)
async def accept_room_booking(
    room_id: int, booking_id: int, uuid: int = Depends(get_uuid_from_xtoken)
):
    booking_path = f"/rooms/{room_id}/bookings/{booking_id}"
    booking, _ = Requester.room_srv_fetch("GET", booking_path, {HTTP_200_OK})

    if not AuthSender.has_permission_to_modify(uuid, booking["user_id"]):
        raise UnauthorizedRequestError("Can't accept other users bookings")

    path = f"/bookings/{booking_id}/accept/"
    book_accepted, _ = Requester.payment_fetch("POST", path, {HTTP_200_OK})

    # Update status to confirmed in post server
    booking_status = {"status": book_accepted["bookingStatus"]}
    booking, _ = Requester.room_srv_fetch(
        "PATCH", booking_path, {HTTP_200_OK}, payload=booking_status
    )

    return booking


@router.post(
    "/rooms/{room_id}/bookings/{booking_id}/reject",
    response_model=RoomBookingDB,
    status_code=HTTP_200_OK,
)
async def reject_room_booking(
    room_id: int, booking_id: int, uuid: int = Depends(get_uuid_from_xtoken)
):
    booking_path = f"/rooms/{room_id}/bookings/{booking_id}"
    booking, _ = Requester.room_srv_fetch("GET", booking_path, {HTTP_200_OK})

    if not AuthSender.has_permission_to_modify(uuid, booking["user_id"]):
        raise UnauthorizedRequestError("Can't reject other users bookings")

    path = f"/bookings/{booking_id}/reject/"
    book_rejected, _ = Requester.payment_fetch("POST", path, {HTTP_200_OK})

    # Delete the rejected booking in post server and user server
    booking, _ = Requester.room_srv_fetch("DELETE", booking_path, {HTTP_200_OK})

    user_path = f"/users/{uuid}/bookings/{booking_id}"
    Requester.user_srv_fetch("DELETE", user_path, {HTTP_200_OK})

    return booking


@router.get(
    "/rooms/{room_id}/bookings/{booking_id}",
    response_model=RoomBookingDB,
    status_code=HTTP_200_OK,
)
async def get_room_booking(room_id: int, booking_id: int):
    path = f"/rooms/{room_id}/bookings/{booking_id}"
    booking, _ = Requester.room_srv_fetch("GET", path, {HTTP_200_OK})

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
    booking, _ = Requester.room_srv_fetch("GET", booking_path, {HTTP_200_OK})

    if not AuthSender.has_permission_to_modify(uuid, booking["user_id"]):
        raise UnauthorizedRequestError("Can't delete other users bookings")

    booking, _ = Requester.room_srv_fetch("DELETE", booking_path, {HTTP_200_OK})

    user_path = f"/users/{uuid}/bookings/{booking_id}"
    Requester.user_srv_fetch("DELETE", user_path, {HTTP_200_OK})

    return booking


@router.get(
    "/users/{room_id}/bookings/{booking_id}",
    response_model=UserBooking,
    status_code=HTTP_200_OK,
)
async def get_user_booking(room_id: int, booking_id: int):
    path = f"/users/{room_id}/bookings/{booking_id}"
    booking, _ = Requester.user_srv_fetch("GET", path, {HTTP_200_OK})

    return booking


@router.get(
    "/users/{room_id}/bookings", response_model=UserBookingList, status_code=HTTP_200_OK
)
async def get_all_user_bookings(room_id: int):
    path = f"/users/{room_id}/bookings"
    bookings, _ = Requester.user_srv_fetch("GET", path, {HTTP_200_OK})

    return bookings
