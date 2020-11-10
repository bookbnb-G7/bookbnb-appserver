import requests as rq
from fastapi import APIRouter, Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from app.api.models.user_model import UserSchema
from app.api.models.user_rating_model import (
    UserRatingSchema,
    UserRatingList,
)
from app.api.models.user_review_model import UserReviewSchema, UserReviewList

router = APIRouter()
API_URL = "https://bookbnb-userserver.herokuapp.com/users"


@router.post("/", response_model=UserSchema, status_code=HTTP_201_CREATED)
async def create_user(payload: UserSchema, response: Response):
    user = rq.post(API_URL + "/", json=payload.dict())
    response.status_code = user.status_code
    return user.json()


@router.get("/{user_id}", response_model=UserSchema, status_code=HTTP_200_OK)
async def get_user(user_id: int, response: Response):
    user = rq.get(API_URL + f"/{user_id}")
    response.status_code = user.status_code
    return user.json()


@router.post(
    "/{user_id}/host_reviews",
    response_model=UserReviewSchema,
    status_code=HTTP_201_CREATED,
)
async def create_host_review(
    payload: UserReviewSchema, user_id: int, response: Response
):
    review = rq.post(API_URL + f"/{user_id}/host_reviews", json=payload.dict())
    response.status_code = review.status_code
    return review.json()


@router.post(
    "/{user_id}/host_ratings",
    response_model=UserRatingSchema,
    status_code=HTTP_201_CREATED,
)
async def create_host_rating(
    payload: UserRatingSchema, user_id: int, response: Response
):
    rating = rq.post(API_URL + f"/{user_id}/host_ratings", json=payload.dict())
    response.status_code = rating.status_code
    return rating.json()


@router.post(
    "/{user_id}/guest_reviews",
    response_model=UserReviewSchema,
    status_code=HTTP_201_CREATED,
)
async def create_guest_review(
    payload: UserReviewSchema, user_id: int, response: Response
):
    review = rq.post(API_URL + f"/{user_id}/guest_reviews", json=payload.dict())
    response.status_code = review.status_code
    return review.json()


@router.post(
    "/{user_id}/guest_ratings",
    response_model=UserRatingSchema,
    status_code=HTTP_201_CREATED,
)
async def create_guest_rating(
    payload: UserRatingSchema, user_id: int, response: Response
):
    rating = rq.post(API_URL + f"/{user_id}/guest_ratings", json=payload.dict())
    response.status_code = rating.status_code
    return rating.json()


@router.get(
    "/{user_id}/host_reviews", response_model=UserReviewList, status_code=HTTP_200_OK
)
async def get_host_reviews(user_id: int, response: Response):
    review = rq.get(API_URL + f"/{user_id}/host_reviews")
    response.status_code = review.status_code
    return review.json()


@router.get(
    "/{user_id}/host_ratings", response_model=UserRatingList, status_code=HTTP_200_OK
)
async def get_host_ratings(user_id: int, response: Response):
    rating = rq.get(API_URL + f"/{user_id}/host_ratings")
    response.status_code = rating.status_code
    return rating.json()


@router.get(
    "/{user_id}/guest_reviews", response_model=UserReviewList, status_code=HTTP_200_OK
)
async def get_guest_reviews(user_id: int, response: Response):
    review = rq.get(API_URL + f"/{user_id}/guest_reviews")
    response.status_code = review.status_code
    return review.json()


@router.get(
    "/{user_id}/guest_ratings", response_model=UserRatingList, status_code=HTTP_200_OK
)
async def get_guest_ratings(user_id: int, response: Response):
    rating = rq.get(API_URL + f"/{user_id}/guest_ratings")
    response.status_code = rating.status_code
    return rating.json()


@router.get(
    "/{user_id}/host_reviews/{review_id}",
    response_model=UserReviewSchema,
    status_code=HTTP_200_OK,
)
async def get_single_host_review(user_id: int, review_id: int, response: Response):
    review = rq.get(API_URL + f"/{user_id}/host_reviews/{review_id}")
    response.status_code = review.status_code
    return review.json()


@router.get(
    "/{user_id}/host_ratings/{rating_id}",
    response_model=UserRatingSchema,
    status_code=HTTP_200_OK,
)
async def get_single_host_rating(user_id: int, rating_id: int, response: Response):
    rating = rq.get(API_URL + f"/{user_id}/host_ratings/{rating_id}")
    response.status_code = rating.status_code
    return rating.json()


@router.get(
    "/{user_id}/guest_reviews/{review_id}",
    response_model=UserReviewSchema,
    status_code=HTTP_200_OK,
)
async def get_single_guest_review(user_id: int, review_id: int, response: Response):
    review = rq.get(API_URL + f"/{user_id}/guest_reviews/{review_id}")
    response.status_code = review.status_code
    return review.json()


@router.get(
    "/{user_id}/guest_ratings/{rating_id}",
    response_model=UserRatingSchema,
    status_code=HTTP_200_OK,
)
async def get_single_guest_rating(user_id: int, rating_id: int, response: Response):
    rating = rq.get(API_URL + f"/{user_id}/guest_ratings/{rating_id}")
    response.status_code = rating.status_code
    return rating.json()
