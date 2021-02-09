from typing import List, Optional

from app.api.crud.room_photo_dao import RoomPhotoDAO
from app.api.models.room_comment_model import (RoomCommentDB, RoomCommentList,
                                               RoomCommentSchema)
from app.api.models.room_model import RoomDB, RoomList, RoomSchema, RoomUpdate
from app.api.models.room_photo_model import RoomPhoto, RoomPhotoList
from app.api.models.room_rating_model import (RoomRatingDB, RoomRatingList,
                                              RoomRatingSchema)
from app.api.models.room_review_model import (RoomReviewDB, RoomReviewList,
                                              RoomReviewSchema)
from app.db import get_db
from app.dependencies import check_token, get_uuid_from_xtoken
from app.errors.http_error import (BadRequestError, NotFoundError,
                                   UnauthorizedRequestError)
from app.services.authsender import AuthSender
from app.services.photouploader import photouploader
from app.services.requester import Requester
from app.services.notifier import notifier
from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

router = APIRouter()


# -----------------------------------ROOMS------------------------------------- #
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

    payment_payload = {
        "ownerId": req_payload["owner_uuid"],
        "price": req_payload["price_per_day"],
    }

    # Create room in payment server and generate an ID
    room_pay_srv, _ = Requester.payment_fetch(
        method="POST",
        path="/rooms",
        expected_statuses={HTTP_201_CREATED},
        payload=payment_payload,
    )

    # Add id to the room created in room server
    req_payload["id"] = room_pay_srv["id"]

    room, _ = Requester.room_srv_fetch(
        method="POST",
        path="/rooms",
        expected_statuses={HTTP_201_CREATED},
        payload=req_payload,
    )

    del room["blocked"]

    return room


@router.get("", response_model=RoomList, status_code=HTTP_200_OK)
async def get_all_rooms(
    date_begins: Optional[str] = None,
    date_ends: Optional[str] = None,
    longitude: Optional[float] = None,
    latitude: Optional[float] = None,
    people: Optional[int] = None,
    types: List[str] = Query(None),
    max_price: Optional[int] = None,
    min_price: Optional[int] = None,
):
    query = "?"
    path = "/rooms"

    if date_begins is not None:
        query = query + f"date_begins={date_begins}&"

    if date_ends is not None:
        query = query + f"date_ends={date_ends}&"

    if longitude is not None:
        query = query + f"longitude={longitude}&"

    if latitude is not None:
        query = query + f"latitude={latitude}&"

    if people is not None:
        query = query + f"people={people}&"

    if types is not None:
        for type in types:
            query = query + f"types={type}&"

    if min_price is not None:
        query = query + f"min_price={min_price}&"

    if max_price is not None:
        query = query + f"max_price={max_price}&"

    if len(query) > 1:
        # strip last & in the query
        query = query[: (len(query) - 1)]
        path = path + "/" + query

    rooms, _ = Requester.room_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )

    for room in rooms["rooms"]:
        del room["blocked"]

    return rooms


@router.get("/{room_id}", response_model=RoomDB, status_code=HTTP_200_OK)
async def get_room(room_id: int):
    path = f"/rooms/{room_id}"
    room, _ = Requester.room_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )

    del room["blocked"]

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

    del room["blocked"]

    # TODO: Patch room price in payment server

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

    del room["blocked"]

    room_pay, _ = Requester.payment_fetch(
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

    # Send notification
    notifier.send_new_room_rating_notification(
        reviewer_name, room["title"], rating_req_payload["rating"], room["owner_uuid"]
    )

    return rating


@router.get(
    "/{room_id}/ratings/{rating_id}",
    response_model=RoomRatingDB,
    status_code=HTTP_200_OK,
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

    # Send notification
    notifier.send_new_room_review_notification(
        reviewer_name, room["title"], room["owner_uuid"]
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


# -----------------------------ROOMS-COMMENTS-----------------------------------#
@router.post(
    "/{room_id}/comments",
    response_model=RoomCommentDB,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def create_room_comment(
    payload: RoomCommentSchema,
    room_id: int,
    viewer_uuid: int = Depends(get_uuid_from_xtoken),
):
    room_path = "/rooms" + f"/{room_id}"
    room, _ = Requester.room_srv_fetch(
        method="GET", path=room_path, expected_statuses={HTTP_200_OK}
    )

    if (
        (payload.dict()["main_comment_id"] is None) and
        (not AuthSender.has_permission_to_comment(viewer_uuid, room["owner_uuid"]))
    ):
        raise BadRequestError("You can't comment your own rooms!")

    user_path = "/users" + f"/{viewer_uuid}"
    user, _ = Requester.user_srv_fetch(
        method="GET", path=user_path, expected_statuses={HTTP_200_OK}
    )
    commentator = f"{user['firstname']} {user['lastname']}"

    comment_payload = payload.dict()
    comment_payload.update({"commentator": commentator, "commentator_id": viewer_uuid})

    comment_path = "/rooms" + f"/{room_id}/comments"
    comment, _ = Requester.room_srv_fetch(
        method="POST",
        path=comment_path,
        expected_statuses={HTTP_201_CREATED},
        payload=comment_payload,
    )

    # Send notifications
    if (comment_payload["main_comment_id"] is None):
        # send notification to room_owner
        notifier.send_new_comment_notification(
            commentator, room["title"], room["owner_uuid"]
        )
    elif (viewer_uuid == room["owner_uuid"]):
        # send notification answer to main_comment_owner
        main_comment, _ = Requester.room_srv_fetch(
            method="GET",
            path=comment_path + f'/{comment_payload["main_comment_id"]}',
            expected_statuses={HTTP_200_OK}
        )
        notifier.send_answered_comment_notification(
            commentator, room["title"], main_comment["commentator_id"]
        )
    else:
        # send notification answer to owner
        notifier.send_answered_comment_notification(
            commentator, room["title"], room["owner_uuid"]
        )

    return comment


@router.get(
    "/{room_id}/comments", response_model=RoomCommentList, status_code=HTTP_200_OK
)
async def get_all_room_comments(room_id: int):
    path = "/rooms" + f"/{room_id}/comments"
    comments, _ = Requester.room_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return comments


@router.delete(
    "/{room_id}/comments/{comment_id}",
    response_model=RoomCommentDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_room_comment(
    room_id: int,
    comment_id: int,
    viewer_uuid: int = Depends(get_uuid_from_xtoken),
):
    comment_path = f"/rooms/{room_id}/comments/{comment_id}"
    comment, _ = Requester.room_srv_fetch(
        method="GET", path=comment_path, expected_statuses={HTTP_200_OK}
    )

    if not AuthSender.has_permission_to_modify(viewer_uuid, comment["commentator_id"]):
        raise BadRequestError("You can't delete other users room comments!")

    comment, _ = Requester.room_srv_fetch(
        method="DELETE", path=comment_path, expected_statuses={HTTP_200_OK}
    )
    return comment


# ------------------------------------------------------------------------------#


# -----------------------------ROOMS-PHOTOS------------------------------------ #
@router.post(
    "/{room_id}/photos",
    response_model=RoomPhoto,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def add_room_picture(
    room_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    uuid: int = Depends(get_uuid_from_xtoken),
):
    room_path = f"/rooms/{room_id}"
    room, _ = Requester.room_srv_fetch("GET", room_path, {HTTP_200_OK})

    if not AuthSender.has_permission_to_modify(room["owner_uuid"], uuid):
        raise UnauthorizedRequestError("You can't add photos to another user room!")

    image_url, firebase_id = photouploader.upload_room_photo(file, room_id)

    room_photo_path = f"/rooms/{room_id}/photos"
    new_photo_request = {"url": image_url, "firebase_id": firebase_id}
    photo_response, _ = Requester.room_srv_fetch(
        "POST", room_photo_path, {HTTP_201_CREATED}, payload=new_photo_request
    )
    photo_id = photo_response["id"]

    RoomPhotoDAO.add_new_room_photo(db, firebase_id, photo_id)
    return photo_response


@router.get("/{room_id}/photos", response_model=RoomPhotoList, status_code=HTTP_200_OK)
async def get_all_room_photos(
    room_id: int,
):
    room_photo_path = f"/rooms/{room_id}/photos"
    photo_response, _ = Requester.room_srv_fetch("GET", room_photo_path, {HTTP_200_OK})
    return photo_response


@router.get(
    "/{room_id}/photos/{firebase_id}",
    response_model=RoomPhoto,
    status_code=HTTP_200_OK,
)
async def get_room_photo(
    room_id: int,
    firebase_id: int,
    db: Session = Depends(get_db),
):
    photo = RoomPhotoDAO.get_room_photo(db, firebase_id)

    photo_id = photo["room_photo_id"]
    room_photo_path = f"/rooms/{room_id}/photos/{photo_id}"

    photo_response, _ = Requester.room_srv_fetch("GET", room_photo_path, {HTTP_200_OK})
    return photo_response


@router.delete(
    "/{room_id}/photos/{firebase_id}",
    response_model=RoomPhoto,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_room_photo(
    room_id: int,
    firebase_id: int,
    db: Session = Depends(get_db),
    uuid: int = Depends(get_uuid_from_xtoken),
):
    room_path = f"/rooms/{room_id}"
    room, _ = Requester.room_srv_fetch("GET", room_path, {HTTP_200_OK})

    if not AuthSender.has_permission_to_modify(room["owner_uuid"], uuid):
        raise UnauthorizedRequestError("You can't delete photos of another user room!")

    photo = RoomPhotoDAO.delete_room_photo(db, firebase_id)
    if photo is None:
        raise NotFoundError("Photo id")
    photo_id = photo["room_photo_id"]

    room_photo_path = f"/rooms/{room_id}/photos/{photo_id}"
    photo_response, _ = Requester.room_srv_fetch(
        "DELETE", room_photo_path, {HTTP_200_OK}
    )
    return photo_response


# ----------------------------------------------------------------------------- ww#
