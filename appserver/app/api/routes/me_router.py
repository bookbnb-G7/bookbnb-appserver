from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK
from app.services.requester import Requester
from app.api.models.user_model import UserDB, WalletDB
from app.api.models.booking_model import BookingsUserList
from app.api.models.room_model import RoomList
from app.dependencies import check_token, get_uuid_from_xtoken

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
    "",
    response_model=UserDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def get_current_user(uuid: int = Depends(get_uuid_from_xtoken)):
    path = f"/users/{uuid}"
    user, _ = Requester.user_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return user


@router.get(
    "/wallet",
    response_model=WalletDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def get_current_user_wallet(uuid: int = Depends(get_uuid_from_xtoken)):
    path = f"/wallets/{uuid}"
    wallet, _ = Requester.payment_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return wallet


@router.get(
    "/bookings",
    response_model=BookingsUserList,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def get_current_user_bookings(uuid: int = Depends(get_uuid_from_xtoken)):
    path = f"/bookings?roomOwnerId={uuid}"
    bookings_received, _ = Requester.payment_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    path = f"/bookings?bookerId={uuid}"
    bookings_made, _ = Requester.payment_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )

    # TODO: Change BookingDB model to match camelcase in payment server
    for i in range(len(bookings_made)):
        bookings_made[i] = payment_camel_to_snake(bookings_made[i])

    for i in range(len(bookings_received)):
        bookings_received[i] = payment_camel_to_snake(bookings_received[i])

    bookings = {
        "made": {
            "amount": len(bookings_made),
            "bookings": bookings_made,
        },
        "received": {
            "amount": len(bookings_received),
            "bookings": bookings_received,
        }
    }

    return bookings


@router.get(
    "/rooms",
    response_model=RoomList,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def get_current_user_rooms(uuid: int = Depends(get_uuid_from_xtoken)):
    path = f"/rooms?owner_uuid={uuid}"
    rooms, _ = Requester.room_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )

    return rooms
