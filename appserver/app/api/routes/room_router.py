import requests as rq
from fastapi import APIRouter, Response
from app.api.models.room_model import RoomSchema, RoomDB
from app.api.models.room_rating_model import (
    RoomRatingDB,
    RoomRatingSchema,
    RoomRatingList,
)
from app.api.models.room_review_model import (
    RoomReviewDB,
    RoomReviewSchema,
    RoomReviewList,
)


router = APIRouter()
# API_URL = "https://bookbnb-postserver.herokuapp.com/rooms"
API_URL = "http://localhost:4000/rooms"


# Fix: Ver si hace falta agregar el status code al decorator para que genere la doc
@router.post("/", response_model=RoomDB)
async def create_room(payload: RoomSchema, response: Response):
    room = rq.post(API_URL + "/", json=payload.dict())
    response.status_code = room.status_code
    return room.json()


@router.post("/{room_id}/ratings", response_model=RoomRatingDB)
async def rate_room(payload: RoomRatingSchema, room_id: int, response: Response):
    room = rq.post(API_URL + f"/{room_id}/ratings", json=payload.dict())
    response.status_code = room.status_code
    return room.json()


@router.post("/{room_id}/reviews", response_model=RoomReviewDB)
async def review_room(payload: RoomReviewSchema, room_id: int, response: Response):
    room = rq.post(API_URL + f"/{room_id}/reviews", json=payload.dict())
    response.status_code = room.status_code
    return room.json()


@router.get("/{room_id}", response_model=RoomDB)
async def get_room(room_id: int, response: Response):
    room = rq.get(API_URL + f"/{room_id}")
    response.status_code = room.status_code
    return room.json()


@router.get("/{room_id}/reviews/{review_id}", response_model=RoomReviewDB)
async def get_room_review(room_id: int, review_id: int, response: Response):
    room = rq.get(API_URL + f"/{room_id}/reviews/{review_id}")
    response.status_code = room.status_code
    return room.json()


@router.get("/{room_id}/ratings/{rating_id}", response_model=RoomRatingDB)
async def get_room_rating(room_id: int, rating_id: int, response: Response):
    room = rq.get(API_URL + f"/{room_id}/ratings/{rating_id}")
    response.status_code = room.status_code
    return room.json()


@router.get("/{room_id}/ratings", response_model=RoomRatingList)
async def get_all_room_ratings(room_id: int, response: Response):
    room = rq.get(API_URL + f"/{room_id}/ratings")
    response.status_code = room.status_code
    return room.json()


@router.get("/{room_id}/reviews", response_model=RoomReviewList)
async def get_all_room_reviews(room_id: int, response: Response):
    room = rq.get(API_URL + f"/{room_id}/reviews")
    response.status_code = room.status_code
    return room.json()
