import logging

from app.api.models.bookings_models import (BookingDB,
                                            BookingList,
                                            BookingSchema)

from typing import Optional
from app.dependencies import check_token, get_uuid_from_xtoken

from app.errors.http_error import (NotAllowedRequestError,
                                   UnauthorizedRequestError)

from fastapi import APIRouter, Depends
from app.services.requester import Requester
from app.services.authsender import AuthSender
from starlette.status import (HTTP_200_OK,
                              HTTP_201_CREATED,
                              HTTP_404_NOT_FOUND)

logger = logging.getLogger(__name__)
router = APIRouter()


def payment_camel_to_snake(payment_payload):
    booking_camel = {
        "id": payment_payload["id"],
        "price": payment_payload["price"],
        "room_id": payment_payload["roomId"],
        "booker_id": payment_payload["bookerId"],
        "room_owner_id": payment_payload["roomOwnerId"],
        "date_from": payment_payload["dateFrom"],
        "date_to": payment_payload["dateTo"],
        "booking_status": payment_payload["bookingStatus"],
        "transaction_hash": payment_payload["transactionHash"],
        "transaction_status": payment_payload["transactionStatus"]
    }

    return booking_camel


@router.get(
    "", response_model=BookingList, status_code=HTTP_200_OK
)
async def get_all_bookings(
    bookerId: Optional[int] = None,
    roomOwnerId: Optional[int] = None,
    roomId: Optional[int] = None,
    bookingStatus: Optional[int] = None,
):
    query = "?"
    path = ""

    if bookerId is not None:
        query = query + f"bookerId={bookerId}&"

    if roomOwnerId is not None:
        query = query + f"roomOwnerId={roomOwnerId}&"

    if roomId is not None:
        query = query + f"roomId={roomId}&"

    if bookingStatus is not None:
        query = query + f"bookingStatus={bookingStatus}&"

    if len(query) > 1:
        # strip last & in the query
        query = query[: (len(query) - 1)]
        path = path + "/" + query

    bookings, _ = Requester.payment_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )

    # TODO: Change BookingDB model to match camelcase in payment server
    for i in range(len(bookings)):
        bookings[i] = payment_camel_to_snake(bookings[i])

    booking_list = {
        "amount": len(bookings),
        "bookings": bookings
    }

    return booking_list


@router.post(
    "",
    response_model=BookingDB,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def create_new_booking(
    payload: BookingSchema,
    uuid: int = Depends(get_uuid_from_xtoken),
):

    room_id = payload.room_id
    room_path = f"/rooms/{room_id}"
    room, _ = Requester.room_srv_fetch("GET", room_path, {HTTP_200_OK})

    if not AuthSender.can_book_room(room["owner_uuid"], uuid):
        raise NotAllowedRequestError("Can't create booking of your own room")

    # Create intent book in payment server

    booking_path = "/bookings"
    payload_booking = {
        "bookerId": uuid,
        "roomId": room_id,
        "dateFrom": payload.date_from.strftime('%d-%m-%Y'),
        "dateTo": payload.date_to.strftime('%d-%m-%Y')
    }
    booking, _ = Requester.payment_fetch(
        method="POST",
        path=booking_path,
        expected_statuses={HTTP_201_CREATED},
        payload=payload_booking
    )

    # Create booking in room server
    booking_path = f"/rooms/{room_id}/bookings"
    # Add the booking id received from the payment server
    payload_booking = {
        "id": booking["id"],
        "date_from": payload.date_from.strftime('%Y-%m-%d'),
        "date_to": payload.date_to.strftime('%Y-%m-%d')
    }

    booking_room, _ = Requester.room_srv_fetch(
        "POST", booking_path, {HTTP_201_CREATED}, payload=payload_booking
    )

    # TODO: Change BookingDB model to match camelcase in payment server
    booking_camel = payment_camel_to_snake(booking)

    return booking_camel


@router.post(
    "/{booking_id}/accept",
    response_model=BookingDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def accept_booking(
    booking_id: int,
    uuid: int = Depends(get_uuid_from_xtoken)
):
    path = f"/bookings/{booking_id}"
    booking, _ = Requester.payment_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    room_owner_id = booking["roomOwnerId"]

    if not AuthSender.has_permission_to_modify(uuid, room_owner_id):
        raise UnauthorizedRequestError("Can't accept other users bookings")

    path = f"/bookings/{booking_id}/accept"
    payload_accept = {"roomOwnerId": room_owner_id}
    book_accepted, _ = Requester.payment_fetch(
        "POST", path, {HTTP_200_OK}, payload=payload_accept
    )

    # TODO: Change BookingDB model to match camelcase in payment server
    booking_camel = payment_camel_to_snake(book_accepted)

    return booking_camel


@router.post(
    "/{booking_id}/reject",
    response_model=BookingDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def reject_booking(
    booking_id: int,
    uuid: int = Depends(get_uuid_from_xtoken)
):
    path = f"/bookings/{booking_id}"
    booking, _ = Requester.payment_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    room_id = booking["roomId"]
    room_owner_id = booking["roomOwnerId"]

    if not AuthSender.has_permission_to_modify(uuid, room_owner_id):
        raise UnauthorizedRequestError("Can't reject other users bookings")

    path = f"/bookings/{booking_id}/reject"
    payload_reject = {"roomOwnerId": room_owner_id}
    book_rejected, _ = Requester.payment_fetch(
        "POST", path, {HTTP_200_OK}, payload=payload_reject
    )

    # Delete the rejected booking in post server
    booking_path = f"/rooms/{room_id}/bookings/{booking_id}"
    booking, _ = Requester.room_srv_fetch(
        "DELETE", booking_path, {HTTP_200_OK}
    )

    # TODO: Change BookingDB model to match camelcase in payment server
    booking_camel = payment_camel_to_snake(book_rejected)

    return booking_camel


@router.get(
    "/{booking_id}",
    response_model=BookingDB,
    status_code=HTTP_200_OK,
)
async def get_booking(booking_id: int):
    path = f"/bookings/{booking_id}"
    booking, _ = Requester.payment_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )

    # TODO: Change BookingDB model to match camelcase in payment server
    booking_camel = payment_camel_to_snake(booking)

    return booking_camel


@router.delete(
    "/{booking_id}",
    response_model=BookingDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_booking(
    booking_id: int,
    uuid: int = Depends(get_uuid_from_xtoken)
):
    path = f"/bookings/{booking_id}"
    booking, _ = Requester.payment_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    room_id = booking["roomId"]
    room_owner_id = booking["roomOwnerId"]

    if not AuthSender.has_permission_to_modify(uuid, room_owner_id):
        raise UnauthorizedRequestError("Can't reject other users bookings")

    path = f"/bookings/{booking_id}"
    book_deleted, _ = Requester.payment_fetch(
        "DELETE", path, {HTTP_200_OK}
    )

    # Delete the rejected booking in post server,
    # if it is not found it is also OK!
    booking_path = f"/rooms/{room_id}/bookings/{booking_id}"
    booking, _ = Requester.room_srv_fetch(
        "DELETE", booking_path, {HTTP_200_OK, HTTP_404_NOT_FOUND}
    )

    # TODO: Change BookingDB model to match camelcase in payment server
    booking_camel = payment_camel_to_snake(book_deleted)

    return booking_camel
