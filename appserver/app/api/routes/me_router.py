from app.api.models.booking_model import BookingsUserList
from app.api.models.chat_model import (ChatDB, ChatList, MessageDB,
                                       MessageSchema)
from app.api.models.room_model import RoomDB, RoomList
from app.api.models.token_model import TokenSchema
from app.api.models.user_model import UserDB, UserSchema, WalletDB
from app.api.models.user_favorite_room_model import UserFavoriteRoomSchema
from app.dependencies import check_token, get_uuid_from_xtoken
from app.services.chat import chat_service
from app.services.notifier import notifier
from app.services.photouploader import photouploader
from app.services.requester import Requester
from fastapi import APIRouter, Depends, File, Response, UploadFile
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

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
        "transaction_status": payment_payload["transactionStatus"],
        "created_at": payment_payload["createdAt"],
        "updated_at": payment_payload["updatedAt"],
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
        },
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


@router.post(
    "/token",
    response_model=TokenSchema,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def set_push_token(
    payload: TokenSchema, uuid: int = Depends(get_uuid_from_xtoken)
):
    notifier.set_push_token(uuid, payload.dict()["push_token"])
    return payload


@router.get(
    "/token",
    response_model=TokenSchema,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def get_push_token(uuid: int = Depends(get_uuid_from_xtoken)):
    push_token = notifier.get_push_token(uuid)
    return {"push_token": push_token}


@router.delete(
    "/token",
    response_model=TokenSchema,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_push_token(uuid: int = Depends(get_uuid_from_xtoken)):
    removed_token = notifier.remove_push_token(uuid)
    return {"push_token": removed_token}


@router.post(
    "/profile_picture",
    response_model=UserSchema,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def update_profile_photo(
    _response: Response,
    file: UploadFile = File(...),
    uuid: int = Depends(get_uuid_from_xtoken),
):
    image_url = photouploader.upload_profile_photo(file, uuid)

    user_patch = {"photo": image_url}
    user_profile_path = f"/users/{uuid}"
    user_response, _ = Requester.user_srv_fetch(
        "PATCH", user_profile_path, {HTTP_200_OK}, payload=user_patch
    )

    return user_response


@router.get(
    "/chats",
    response_model=ChatList,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def get_all_chats(
    _reponse: Response,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    chats = chat_service.get_all_chats_from(uuid)
    return {"amount": len(chats), "chats": chats}


@router.get(
    "/chats/{other_uuid}",
    response_model=ChatDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def get_chat(
    _reponse: Response,
    other_uuid: int,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    messages = chat_service.get_messages_between(uuid, other_uuid)

    return {"amount": len(messages), "messages": messages}


@router.post(
    "/chats/{other_uuid}",
    response_model=MessageDB,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def send_message(
    _reponse: Response,
    payload: MessageSchema,
    other_uuid: int,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    path = f"/users/{uuid}"
    me, _ = Requester.user_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )

    path = f"/users/{other_uuid}"
    other, _ = Requester.user_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )

    own_name = f"{me['firstname']} {me['lastname']}"
    other_name = f"{other['firstname']} {other['lastname']}"

    own_data = {"name": own_name, "uuid": uuid}
    other_data = {"name": other_name, "uuid": other_uuid}

    return chat_service.send_message(payload.dict()["message"], own_data, other_data)


@router.post(
    "/favorite_rooms",
    response_model=RoomDB,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def create_favorite_room(
    payload: UserFavoriteRoomSchema,
    uuid: int = Depends(get_uuid_from_xtoken),
):

    room_path = f"/rooms/{payload.dict()['room_id']}"
    room, _ = Requester.room_srv_fetch(
        method="GET", path=room_path, expected_statuses={HTTP_200_OK}
    )

    path = f"/users/{uuid}/favorite_rooms"
    favorite_room, _ = Requester.user_srv_fetch(
        method="POST",
        path=path,
        expected_statuses={HTTP_201_CREATED},
        payload=payload.dict(),
    )

    return room


@router.get(
    "/favorite_rooms",
    response_model=RoomList,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def get_favorite_rooms(
    uuid: int = Depends(get_uuid_from_xtoken),
):
    path = f"/users/{uuid}/favorite_rooms"
    favorite_rooms, _ = Requester.user_srv_fetch(
        method="GET",
        path=path,
        expected_statuses={HTTP_200_OK},
    )

    query = "?"
    if len(favorite_rooms["favorites"]) > 0:
        for favorite in favorite_rooms["favorites"]:
            query = query + f"ids={favorite['room_id']}&"
    else:
        query = query + f"ids={-1}"

    room_path = "/rooms" + query
    rooms, _ = Requester.room_srv_fetch(
        method="GET", path=room_path, expected_statuses={HTTP_200_OK}
    )

    return rooms


@router.delete(
    "/favorite_rooms/{favorite_id}",
    response_model=RoomDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_favorite_room(
    favorite_id: int,
    uuid: int = Depends(get_uuid_from_xtoken),
):

    path = f"/users/{uuid}/favorite_rooms/{favorite_id}"
    favorite_room, _ = Requester.user_srv_fetch(
        method="GET",
        path=path,
        expected_statuses={HTTP_200_OK},
    )

    room_path = f"/rooms/{favorite_room['room_id']}"
    room, _ = Requester.room_srv_fetch(
        method="GET", path=room_path, expected_statuses={HTTP_200_OK}
    )

    path = f"/users/{uuid}/favorite_rooms/{favorite_id}"
    favorite_rooms, _ = Requester.user_srv_fetch(
        method="DELETE",
        path=path,
        expected_statuses={HTTP_200_OK},
    )

    return room

