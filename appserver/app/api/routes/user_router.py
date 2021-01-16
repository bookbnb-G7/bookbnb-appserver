from typing import Optional

from app.api.models.user_model import (UserDB, UserListSchema, UserSchema,
                                       UserUpdateSchema)
from app.api.models.user_rating_model import UserRatingList, UserRatingSchema
from app.api.models.user_review_model import UserReviewList, UserReviewSchema
from app.dependencies import check_token, get_uuid_from_xtoken
from app.errors.http_error import UnauthorizedRequestError
from app.services.authsender import AuthSender
from app.services.requester import Requester
from fastapi import APIRouter, Depends, Header
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

router = APIRouter()

# -----------------------------------USERS--------------------------------------#


@router.post(
    "",
    response_model=UserDB,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def create_user(
    payload: UserSchema,
    x_access_token: Optional[str] = Header(None),
):
    auth_payload = {"email": payload.email}
    auth_header = {"x-access-token": x_access_token}
    registered_user, _ = Requester.auth_srv_fetch(
        method="POST",
        path="/user/registered",
        expected_statuses={HTTP_201_CREATED},
        payload=auth_payload,
        extra_headers=auth_header,
    )
    path = "/users"
    payload_user = payload.dict()
    payload_user.update({"id": registered_user["uuid"]})
    user, _ = Requester.user_srv_fetch(
        method="POST",
        path=path,
        expected_statuses={HTTP_201_CREATED},
        payload=payload_user,
    )

    # create wallet
    path = "/wallets"
    payload_wallet = {"uuid": registered_user["uuid"]}
    wallet, _ = Requester.payment_fetch(
        method="POST",
        path=path,
        expected_statuses={HTTP_201_CREATED},
        payload=payload_wallet,
    )

    return user


@router.get("/{user_id}", response_model=UserDB, status_code=HTTP_200_OK)
async def get_user(user_id: int):
    path = f"/users/{user_id}"
    user, _ = Requester.user_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return user


@router.patch(
    "/{user_id}",
    response_model=UserSchema,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def update_user(
    user_id: int,
    payload: UserUpdateSchema,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't update info about other users")

    path = f"/users/{user_id}"
    new_user_info, _ = Requester.user_srv_fetch(
        method="PATCH",
        path=path,
        expected_statuses={HTTP_200_OK},
        payload=payload.dict(exclude_unset=True),
    )
    return new_user_info


@router.delete(
    "/{user_id}", status_code=HTTP_200_OK, dependencies=[Depends(check_token)]
)
async def delete_user(user_id: int, uuid: int = Depends(get_uuid_from_xtoken)):
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't delete other users")

    path = f"/users/{user_id}"
    new_user_info, _ = Requester.user_srv_fetch(
        method="DELETE", path=path, expected_statuses={HTTP_200_OK}
    )

    auth_path = f"/user/registered/{uuid}"
    Requester.auth_srv_fetch("DELETE", path=auth_path, expected_statuses={HTTP_200_OK})

    return new_user_info


@router.get("", response_model=UserListSchema, status_code=HTTP_200_OK)
async def get_all_users():
    path = "/users"
    users, _ = Requester.user_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return users


# ------------------------------------------------------------------------------#


# --------------------------RATINGS/REVIEWS-------------------------------------#


@router.post(
    "/{user_id}/host_reviews",
    response_model=UserReviewSchema,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def create_host_review(
    payload: UserReviewSchema,
    user_id: int,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't create a review of other user")

    path = f"/users/{user_id}/host_reviews"
    review, _ = Requester.user_srv_fetch(
        method="POST",
        path=path,
        expected_statuses={HTTP_201_CREATED},
        payload=payload.dict(),
    )

    return review


@router.post(
    "/{user_id}/host_ratings",
    response_model=UserRatingSchema,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def create_host_rating(
    payload: UserRatingSchema,
    user_id: int,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't create a rating of other user")

    path = f"/users/{user_id}/host_ratings"
    rating, _ = Requester.user_srv_fetch(
        method="POST",
        path=path,
        expected_statuses={HTTP_201_CREATED},
        payload=payload.dict(),
    )

    return rating


@router.post(
    "/{user_id}/guest_reviews",
    response_model=UserReviewSchema,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def create_guest_review(
    payload: UserReviewSchema,
    user_id: int,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't create a review of other user")

    path = f"/users/{user_id}/guest_reviews"
    review, _ = Requester.user_srv_fetch(
        method="POST",
        path=path,
        expected_statuses={HTTP_201_CREATED},
        payload=payload.dict(),
    )

    return review


@router.post(
    "/{user_id}/guest_ratings",
    response_model=UserRatingSchema,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def create_guest_rating(
    payload: UserRatingSchema,
    user_id: int,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't create a rating of other user")

    path = f"/users/{user_id}/guest_ratings"
    rating, _ = Requester.user_srv_fetch(
        method="POST",
        path=path,
        expected_statuses={HTTP_201_CREATED},
        payload=payload.dict(),
    )

    return rating


@router.get(
    "/{user_id}/host_reviews", response_model=UserReviewList, status_code=HTTP_200_OK
)
async def get_host_reviews(user_id: int):
    path = f"/users/{user_id}/host_reviews"
    user_reviews, _ = Requester.user_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return user_reviews


@router.get(
    "/{user_id}/host_ratings", response_model=UserRatingList, status_code=HTTP_200_OK
)
async def get_host_ratings(user_id: int):
    path = f"/users/{user_id}/host_ratings"
    user_reviews, _ = Requester.user_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return user_reviews


@router.get(
    "/{user_id}/guest_reviews", response_model=UserReviewList, status_code=HTTP_200_OK
)
async def get_guest_reviews(user_id: int):
    path = f"/users/{user_id}/guest_reviews"
    user_reviews, _ = Requester.user_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return user_reviews


@router.get(
    "/{user_id}/guest_ratings", response_model=UserRatingList, status_code=HTTP_200_OK
)
async def get_guest_ratings(user_id: int):
    path = f"/users/{user_id}/guest_ratings"
    user_reviews, _ = Requester.user_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return user_reviews


@router.get(
    "/{user_id}/host_reviews/{review_id}",
    response_model=UserReviewSchema,
    status_code=HTTP_200_OK,
)
async def get_single_host_review(user_id: int, review_id: int):
    path = f"/users/{user_id}/host_reviews/{review_id}"
    user_reviews, _ = Requester.user_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return user_reviews


@router.get(
    "/{user_id}/host_ratings/{rating_id}",
    response_model=UserRatingSchema,
    status_code=HTTP_200_OK,
)
async def get_single_host_rating(user_id: int, rating_id: int):
    path = f"/users/{user_id}/host_ratings/{rating_id}"
    user_reviews, _ = Requester.user_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return user_reviews


@router.get(
    "/{user_id}/guest_reviews/{review_id}",
    response_model=UserReviewSchema,
    status_code=HTTP_200_OK,
)
async def get_single_guest_review(user_id: int, review_id: int):
    path = f"/users/{user_id}/guest_reviews/{review_id}"
    user_reviews, _ = Requester.user_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return user_reviews


@router.get(
    "/{user_id}/guest_ratings/{rating_id}",
    response_model=UserRatingSchema,
    status_code=HTTP_200_OK,
)
async def get_single_guest_rating(user_id: int, rating_id: int):
    path = f"/users/{user_id}/guest_ratings/{rating_id}"
    user_ratings, _ = Requester.user_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return user_ratings


@router.delete(
    "/{user_id}/host_reviews/{review_id}",
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_host_review(
    user_id: int,
    review_id: int,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    review_path = f"/users/{user_id}/host_reviews/{review_id}"
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't delete a review of another user")

    review, _ = Requester.user_srv_fetch(
        method="DELETE", path=review_path, expected_statuses={HTTP_200_OK}
    )
    return review


@router.delete(
    "/{user_id}/host_ratings/{rating_id}",
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_host_rating(
    user_id: int,
    rating_id: int,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    rating_path = f"/users/{user_id}/host_ratings/{rating_id}"
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't delete a rating of another user")

    review, _ = Requester.user_srv_fetch(
        method="DELETE", path=rating_path, expected_statuses={HTTP_200_OK}
    )
    return review


@router.delete(
    "/{user_id}/guest_reviews/{review_id}",
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_guest_review(
    user_id: int,
    review_id: int,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    review_path = f"/users/{user_id}/guest_reviews/{review_id}"
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't delete a review of another user")

    review, _ = Requester.user_srv_fetch(
        method="DELETE", path=review_path, expected_statuses={HTTP_200_OK}
    )
    return review


@router.delete(
    "/{user_id}/guest_ratings/{rating_id}",
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_guest_rating(
    user_id: int,
    rating_id: int,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    rating_path = f"/users/{user_id}/guest_ratings/{rating_id}"
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't delete a rating of another user")

    review, _ = Requester.user_srv_fetch(
        method="DELETE", path=rating_path, expected_statuses={HTTP_200_OK}
    )
    return review


# ----------------------------------------------------------------------------- #
