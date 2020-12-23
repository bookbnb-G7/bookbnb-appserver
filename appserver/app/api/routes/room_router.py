from typing import Optional
from app.api.models.room_model import RoomDB, RoomList, RoomSchema, RoomUpdate
from app.api.models.room_rating_model import (RoomRatingDB, RoomRatingList,
                                              RoomRatingSchema,
                                              RoomRatingUpdate)
from app.api.models.room_review_model import (RoomReviewDB, RoomReviewList,
                                              RoomReviewSchema,
                                              RoomReviewUpdate)
from app.dependencies import check_token, get_uuid_from_xtoken
from app.errors.http_error import BadRequestError
from app.services.authsender import AuthSender
from app.services.requester import Requester
from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

router = APIRouter()

# -----------------------------------ROOMS--------------------------------------#


@router.post(
    "",
    response_model=RoomDB,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def create_room(payload: RoomSchema, uuid: int = Depends(get_uuid_from_xtoken)):
    path = f"/users/{uuid}"
    user, _ = Requester.user_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    owner = f"{user['firstname']} {user['lastname']}"

    req_payload = payload.dict()
    req_payload.update({"owner_uuid": uuid, "owner": owner})
    room, _ = Requester.room_srv_fetch(
        method="POST",
        path="/rooms",
        expected_statuses={HTTP_201_CREATED},
        payload=req_payload,
    )

    return room


@router.get("", response_model=RoomList, status_code=HTTP_200_OK)
async def get_all_rooms(
    date_begins: Optional[str] = None,
    date_ends: Optional[str] = None,
    longitude: Optional[float] = None,
    latitude: Optional[float] = None,
    people: Optional[int] = None
):
    query = "?"
    path = "/rooms"

    if date_begins is not None:
        query = query + f'date_begins={date_begins}&'

    if date_ends is not None:
        query = query + f'date_ends={date_ends}&'

    if longitude is not None:
        query = query + f'longitude={longitude}&'

    if latitude is not None:
        query = query + f'latitude={latitude}&'

    if people is not None:
        query = query + f'people={people}&'

    if len(query) > 1:
        # strip last & in the query
        query = query[:(len(query) - 1)]
        path = path + "/" + query


    rooms, _ = Requester.room_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return rooms


@router.get("/{room_id}", response_model=RoomDB, status_code=HTTP_200_OK)
async def get_room(room_id: int):
    path = f"/rooms/{room_id}"
    room, _ = Requester.room_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return room


@router.patch(
    "/{room_id}",
    response_model=RoomDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def update_room(
    payload: RoomUpdate,
    room_id: int,
    viewer_uuid: int = Depends(get_uuid_from_xtoken),
):
    path = f"/rooms/{room_id}"
    room, _ = Requester.room_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )

    if not AuthSender.has_permission_to_modify(viewer_uuid, room["owner_uuid"]):
        raise BadRequestError("You can't update other users rooms!")

    room_req_payload = payload.dict(exclude_unset=True)

    path = f"/rooms/{room_id}"
    room, _ = Requester.room_srv_fetch(
        method="PATCH",
        path=path,
        expected_statuses={HTTP_200_OK},
        payload=room_req_payload,
    )
    return room


@router.delete(
    "/{room_id}",
    response_model=RoomDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_room(room_id: int, viewer_uuid: int = Depends(get_uuid_from_xtoken)):

    path = "/rooms" + f"/{room_id}"
    room, _ = Requester.room_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )

    if not AuthSender.has_permission_to_modify(viewer_uuid, room["owner_uuid"]):
        raise BadRequestError("You can't delete other users rooms!")

    path = "/rooms" + f"/{room_id}"
    room, _ = Requester.room_srv_fetch(
        method="DELETE", path=path, expected_statuses={HTTP_200_OK}
    )
    return room


# ------------------------------------------------------------------------------#


# -----------------------------ROOMS-RATINGS------------------------------------#


@router.post(
    "/{room_id}/ratings",
    response_model=RoomRatingDB,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def rate_room(
    payload: RoomRatingSchema,
    room_id: int,
    viewer_uuid: int = Depends(get_uuid_from_xtoken),
):
    room_path = f"/rooms/{room_id}"
    room, _ = Requester.room_srv_fetch(
        method="GET", path=room_path, expected_statuses={HTTP_200_OK}
    )

    if not AuthSender.has_permission_to_comment(viewer_uuid, room["owner_uuid"]):
        raise BadRequestError("You can't rate your own rooms!")

    user_path = f"/users/{viewer_uuid}"
    user, _ = Requester.user_srv_fetch(
        method="GET", path=user_path, expected_statuses={HTTP_200_OK}
    )
    reviewer_name = f"{user['firstname']} {user['lastname']}"

    rating_req_payload = payload.dict()
    rating_req_payload.update({"reviewer": reviewer_name, "reviewer_id": viewer_uuid})

    room_rating_path = f"/rooms/{room_id}/ratings"
    rating, _ = Requester.room_srv_fetch(
        method="POST",
        path=room_rating_path,
        expected_statuses={HTTP_201_CREATED},
        payload=rating_req_payload,
    )
    return rating


@router.get(
    "/{room_id}/ratings/{rating_id}",
    status_code=HTTP_200_OK,
    response_model=RoomRatingDB,
)
async def get_room_rating(room_id: int, rating_id: int):

    path = f"/rooms/{room_id}/ratings/{rating_id}"
    rating, _ = Requester.room_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return rating


@router.get(
    "/{room_id}/ratings", response_model=RoomRatingList, status_code=HTTP_200_OK
)
async def get_all_room_ratings(room_id: int):

    path = f"/rooms/{room_id}/ratings"
    ratings, _ = Requester.room_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return ratings


@router.patch(
    "/{room_id}/ratings/{rating_id}",
    response_model=RoomRatingDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def update_room_rating(
    payload: RoomRatingUpdate,
    room_id: int,
    rating_id: int,
    viewer_uuid: int = Depends(get_uuid_from_xtoken),
):
    room_path = f"/rooms/{room_id}/ratings/{rating_id}"
    rating, _ = Requester.room_srv_fetch(
        method="GET", path=room_path, expected_statuses={HTTP_200_OK}
    )

    if not AuthSender.has_permission_to_modify(viewer_uuid, rating["reviewer_id"]):
        raise BadRequestError("You can't update other users room ratings!")

    rating_req_payload = payload.dict(exclude_unset=True)

    rating_path = f"/rooms/{room_id}/ratings/{rating_id}"
    rating, _ = Requester.room_srv_fetch(
        method="PATCH",
        path=rating_path,
        expected_statuses={HTTP_200_OK},
        payload=rating_req_payload,
    )

    return rating


@router.delete(
    "/{room_id}/ratings/{rating_id}",
    response_model=RoomRatingDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_room_rating(
    room_id: int,
    rating_id: int,
    viewer_uuid: int = Depends(get_uuid_from_xtoken),
):

    room_path = f"/rooms/{room_id}/ratings/{rating_id}"
    rating, _ = Requester.room_srv_fetch(
        method="GET", path=room_path, expected_statuses={HTTP_200_OK}
    )

    if not AuthSender.has_permission_to_modify(viewer_uuid, rating["reviewer_id"]):
        raise BadRequestError("You can't delete other users room ratings!")

    rating_path = f"/rooms/{room_id}/ratings/{rating_id}"
    rating, _ = Requester.room_srv_fetch(
        method="DELETE", path=rating_path, expected_statuses={HTTP_200_OK}
    )
    return rating


# ------------------------------------------------------------------------------#


# -----------------------------ROOMS-REVIEWS------------------------------------#


@router.post(
    "/{room_id}/reviews",
    response_model=RoomReviewDB,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def review_room(
    payload: RoomReviewSchema,
    room_id: int,
    viewer_uuid: int = Depends(get_uuid_from_xtoken),
):

    room_path = "/rooms" + f"/{room_id}"
    room, _ = Requester.room_srv_fetch(
        method="GET", path=room_path, expected_statuses={HTTP_200_OK}
    )

    if not AuthSender.has_permission_to_comment(viewer_uuid, room["owner_uuid"]):
        raise BadRequestError("You can't review your own rooms!")

    user_path = "/users" + f"/{viewer_uuid}"
    user, _ = Requester.user_srv_fetch(
        method="GET", path=user_path, expected_statuses={HTTP_200_OK}
    )
    reviewer_name = f"{user['firstname']} {user['lastname']}"

    review_payload = payload.dict()
    review_payload.update({"reviewer": reviewer_name, "reviewer_id": viewer_uuid})

    review_path = "/rooms" + f"/{room_id}/reviews"
    review, _ = Requester.room_srv_fetch(
        method="POST",
        path=review_path,
        expected_statuses={HTTP_201_CREATED},
        payload=review_payload,
    )
    return review


@router.get(
    "/{room_id}/reviews/{review_id}",
    response_model=RoomReviewDB,
    status_code=HTTP_200_OK,
)
async def get_room_review(room_id: int, review_id: int):

    path = "/rooms" + f"/{room_id}/reviews/{review_id}"
    review, _ = Requester.room_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return review


@router.get(
    "/{room_id}/reviews", response_model=RoomReviewList, status_code=HTTP_200_OK
)
async def get_all_room_reviews(room_id: int):

    path = "/rooms" + f"/{room_id}/reviews"
    reviews, _ = Requester.room_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return reviews


@router.patch(
    "/{room_id}/reviews/{review_id}",
    response_model=RoomReviewDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def update_room_review(
    payload: RoomReviewUpdate,
    room_id: int,
    review_id: int,
    viewer_uuid: int = Depends(get_uuid_from_xtoken),
):

    path = f"/rooms/{room_id}/reviews/{review_id}"
    review, _ = Requester.room_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )

    if not AuthSender.has_permission_to_modify(viewer_uuid, review["reviewer_id"]):
        raise BadRequestError("You can't update other users room reviews!")

    review_rew_payload = payload.dict(exclude_unset=True)
    path = f"/rooms/{room_id}/reviews/{review_id}"
    review, _ = Requester.room_srv_fetch(
        method="PATCH",
        path=path,
        expected_statuses={HTTP_200_OK},
        payload=review_rew_payload,
    )
    return review


@router.delete(
    "/{room_id}/reviews/{review_id}",
    response_model=RoomReviewDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_room_review(
    room_id: int,
    review_id: int,
    viewer_uuid: int = Depends(get_uuid_from_xtoken),
):

    review_path = f"/rooms/{room_id}/reviews/{review_id}"
    review, _ = Requester.room_srv_fetch(
        method="GET", path=review_path, expected_statuses={HTTP_200_OK}
    )

    if not AuthSender.has_permission_to_modify(viewer_uuid, review["reviewer_id"]):
        raise BadRequestError("You can't delete other users room reviews!")

    review, _ = Requester.room_srv_fetch(
        method="DELETE", path=review_path, expected_statuses={HTTP_200_OK}
    )
    return review


# ------------------------------------------------------------------------------#
