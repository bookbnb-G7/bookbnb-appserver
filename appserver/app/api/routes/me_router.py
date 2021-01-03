from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK
from app.services.requester import Requester
from app.api.models.user_model import UserDB, WalletDB
from app.api.models.bookings_models import BookingsUserList
from app.api.models.room_model import RoomList
from app.dependencies import check_token, get_uuid_from_xtoken

router = APIRouter()


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

    bookings = {
        "made": bookings_made,
        "received": bookings_received
    }

    return bookings


@router.get(
    "/rooms",
    response_model=RoomList,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def get_current_user_rooms(uuid: int = Depends(get_uuid_from_xtoken)):
    path = f"/rooms/?owner_uuid={uuid}"
    rooms, _ = Requester.room_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )

    return rooms
