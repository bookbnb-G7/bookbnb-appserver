import requests as rq
from fastapi import APIRouter, Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from app.api.models.room_model import RoomSchema, RoomDB, RoomUpdate, RoomList
from app.api.models.room_rating_model import (
    RoomRatingDB,
    RoomRatingSchema,
    RoomRatingList,
    RoomRatingUpdate,
)
from app.api.models.room_review_model import (
    RoomReviewDB,
    RoomReviewSchema,
    RoomReviewList,
    RoomReviewUpdate,
)


router = APIRouter()
API_URL = "https://bookbnb-postserver.herokuapp.com/rooms"


@router.post("/", response_model=RoomDB, status_code=HTTP_201_CREATED)
async def create_room(payload: RoomSchema, response: Response):
    room = rq.post(API_URL + "/", json=payload.dict())
    response.status_code = room.status_code
    return room.json()


@router.get("/", response_model=RoomList, status_code=HTTP_200_OK)
async def get_rooms(response: Response):
    rooms = rq.get(f"{API_URL}/")
    response.status_code = rooms.status_code
    return rooms.json()


@router.post(
    "/{room_id}/ratings", response_model=RoomRatingDB, status_code=HTTP_201_CREATED
)
async def rate_room(payload: RoomRatingSchema, room_id: int, response: Response):
    room = rq.post(API_URL + f"/{room_id}/ratings", json=payload.dict())
    response.status_code = room.status_code
    return room.json()


@router.post(
    "/{room_id}/reviews", response_model=RoomReviewDB, status_code=HTTP_201_CREATED
)
async def review_room(payload: RoomReviewSchema, room_id: int, response: Response):
    room = rq.post(API_URL + f"/{room_id}/reviews", json=payload.dict())
    response.status_code = room.status_code
    return room.json()


@router.get("/{room_id}", response_model=RoomDB, status_code=HTTP_200_OK)
async def get_room(room_id: int, response: Response):
    room = rq.get(API_URL + f"/{room_id}")
    response.status_code = room.status_code
    return room.json()


@router.get(
    "/{room_id}/reviews/{review_id}",
    response_model=RoomReviewDB,
    status_code=HTTP_200_OK,
)
async def get_room_review(room_id: int, review_id: int, response: Response):
    room = rq.get(API_URL + f"/{room_id}/reviews/{review_id}")
    response.status_code = room.status_code
    return room.json()


@router.get(
    "/{room_id}/ratings/{rating_id}",
    response_model=RoomRatingDB,
    status_code=HTTP_200_OK,
)
async def get_room_rating(room_id: int, rating_id: int, response: Response):
    room = rq.get(API_URL + f"/{room_id}/ratings/{rating_id}")
    response.status_code = room.status_code
    return room.json()


@router.get(
    "/{room_id}/ratings", response_model=RoomRatingList, status_code=HTTP_200_OK
)
async def get_all_room_ratings(room_id: int, response: Response):
    room = rq.get(API_URL + f"/{room_id}/ratings")
    response.status_code = room.status_code
    return room.json()


@router.get(
    "/{room_id}/reviews", response_model=RoomReviewList, status_code=HTTP_200_OK
)
async def get_all_room_reviews(room_id: int, response: Response):
    room = rq.get(API_URL + f"/{room_id}/reviews")
    response.status_code = room.status_code
    return room.json()


@router.patch("/{room_id}", response_model=RoomDB, status_code=HTTP_200_OK)
async def update_room(payload: RoomUpdate, room_id: int, response: Response):
    room = rq.patch(API_URL + f"/{room_id}", json=payload.dict(exclude_unset=True))
    response.status_code = room.status_code
    return room.json()


@router.patch(
    "/{room_id}/ratings/{rating_id}",
    response_model=RoomRatingDB,
    status_code=HTTP_200_OK,
)
async def update_room_rating(
    payload: RoomRatingUpdate, room_id: int, rating_id: int, response: Response
):
    room = rq.patch(
        API_URL + f"/{room_id}/ratings/{rating_id}",
        json=payload.dict(exclude_unset=True),
    )
    response.status_code = room.status_code
    return room.json()


@router.patch(
    "/{room_id}/reviews/{review_id}",
    response_model=RoomReviewDB,
    status_code=HTTP_200_OK,
)
async def update_room_review(
    payload: RoomReviewUpdate, room_id: int, review_id: int, response: Response
):
    room = rq.patch(
        API_URL + f"/{room_id}/reviews/{review_id}",
        json=payload.dict(exclude_unset=True),
    )
    response.status_code = room.status_code
    return room.json()


@router.delete("/{room_id}", response_model=RoomDB, status_code=HTTP_200_OK)
async def delete_room(room_id: int, response: Response):
    room = rq.delete(API_URL + f"/{room_id}")
    response.status_code = room.status_code
    return room.json()


@router.delete(
    "/{room_id}/reviews/{review_id}",
    response_model=RoomReviewDB,
    status_code=HTTP_200_OK,
)
async def delete_room_review(room_id: int, review_id: int, response: Response):
    room = rq.delete(API_URL + f"/{room_id}/reviews/{review_id}")
    response.status_code = room.status_code
    return room.json()


@router.delete(
    "/{room_id}/ratings/{rating_id}",
    response_model=RoomRatingDB,
    status_code=HTTP_200_OK,
)
async def delete_room_rating(room_id: int, rating_id: int, response: Response):
    room = rq.delete(API_URL + f"/{room_id}/ratings/{rating_id}")
    response.status_code = room.status_code
    return room.json()
