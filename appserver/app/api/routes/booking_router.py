import logging

from app.api.models.bookings_models import (BookingDB,
                                            BookingList,
                                            BookingSchema)

from app.dependencies import check_token, get_uuid_from_xtoken

from app.errors.http_error import (NotAllowedRequestError,
                                   UnauthorizedRequestError)

from fastapi import APIRouter, Depends
from app.services.requester import Requester
from app.services.authsender import AuthSender
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "", response_model=BookingList, status_code=HTTP_200_OK
)
async def get_all_bookings():
    '''
    return by query params
    '''


@router.post(
    "",
    response_model=BookingDB,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def create_new_booking(
    room_id: int,
    payload: BookingSchema,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    '''
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
    payload_booking["date_begins"] = payload_booking["date_begins"].strftime('%Y-%m-%d')
    payload_booking["date_ends"] = payload_booking["date_ends"].strftime('%Y-%m-%d')
    booking, _ = Requester.room_srv_fetch(
        "POST", booking_path, {HTTP_201_CREATED}, payload=payload_booking
    )

    user_path = f"/users/{uuid}/bookings"
    booking_id = booking["id"]
    user_booking_payload = {"booking_id": booking_id, "room_id": room_id}
    Requester.user_srv_fetch(
        "POST", user_path, {HTTP_201_CREATED}, payload=user_booking_payload
    )

    return booking
    '''


@router.post(
    "/{booking_id}/accept",
    response_model=BookingDB,
    status_code=HTTP_200_OK,
)
async def accept_booking(
    room_id: int, booking_id: int, uuid: int = Depends(get_uuid_from_xtoken)
):
    '''
    room_path = f"/rooms/{room_id}"
    room, _ = Requester.room_srv_fetch("GET", room_path, {HTTP_200_OK})

    if not AuthSender.has_permission_to_modify(uuid, room["owner_uuid"]):
        raise UnauthorizedRequestError("Can't accept other users bookings")

    path = f"/bookings/{booking_id}/accept/"
    payload_accept = {"roomOwnerId": room["owner_uuid"]}
    book_accepted, _ = Requester.payment_fetch("POST", path, {HTTP_200_OK}, payload=payload_accept)

    # Update status to confirmed in post server
    booking_status = {"status": book_accepted["bookingStatus"]}
    booking_path = f"/rooms/{room_id}/bookings/{booking_id}"
    booking, _ = Requester.room_srv_fetch(
        "PATCH", booking_path, {HTTP_200_OK}, payload=booking_status
    )

    return booking
    '''


@router.post(
    "/{booking_id}/reject",
    response_model=BookingDB,
    status_code=HTTP_200_OK,
)
async def reject_booking(
    room_id: int, booking_id: int, uuid: int = Depends(get_uuid_from_xtoken)
):
    '''
    room_path = f"/rooms/{room_id}"
    room, _ = Requester.room_srv_fetch("GET", room_path, {HTTP_200_OK})

    if not AuthSender.has_permission_to_modify(uuid, room["owner_uuid"]):
        raise UnauthorizedRequestError("Can't reject other users bookings")

    path = f"/bookings/{booking_id}/reject/"
    payload_reject = {"roomOwnerId": room["owner_uuid"]}
    book_rejected, _ = Requester.payment_fetch("POST", path, {HTTP_200_OK}, payload=payload_reject)

    # Delete the rejected booking in post server and user server
    booking_path = f"/rooms/{room_id}/bookings/{booking_id}"
    booking, _ = Requester.room_srv_fetch("DELETE", booking_path, {HTTP_200_OK})

    user_path = f"/users/{uuid}/bookings/{booking_id}"
    Requester.user_srv_fetch("DELETE", user_path, {HTTP_200_OK})

    return booking
    '''


@router.get(
    "/{booking_id}",
    response_model=BookingDB,
    status_code=HTTP_200_OK,
)
async def get_booking(room_id: int, booking_id: int):
    '''
    path = f"/rooms/{room_id}/bookings/{booking_id}"
    booking, _ = Requester.room_srv_fetch("GET", path, {HTTP_200_OK})

    return booking
    '''


@router.delete(
    "/{booking_id}",
    response_model=BookingDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_booking(
    room_id: int, booking_id: int, uuid: int = Depends(get_uuid_from_xtoken)
):
    '''
    booking_path = f"/rooms/{room_id}/bookings/{booking_id}"
    booking, _ = Requester.room_srv_fetch("GET", booking_path, {HTTP_200_OK})

    if not AuthSender.has_permission_to_modify(uuid, booking["user_id"]):
        raise UnauthorizedRequestError("Can't delete other users bookings")

    booking, _ = Requester.room_srv_fetch("DELETE", booking_path, {HTTP_200_OK})

    user_path = f"/users/{uuid}/bookings/{booking_id}"
    Requester.user_srv_fetch("DELETE", user_path, {HTTP_200_OK})

    return booking
    '''