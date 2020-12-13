import os
from typing import Optional

from app.api.models.user_model import (UserDB, UserListSchema, UserSchema,
                                       UserUpdateSchema)
from app.api.models.user_rating_model import (UserRatingList, UserRatingSchema,
                                              UserRatingUpdate)
from app.api.models.user_review_model import (UserReviewList, UserReviewSchema,
                                              UserReviewUpdate)
from app.dependencies import check_token, get_uuid_from_xtoken
from app.errors.http_error import UnauthorizedRequestError
from app.services.authsender import AuthSender
from app.services.requester import Requester
from fastapi import APIRouter, Depends, Header, Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

router = APIRouter()
API_URL = os.environ["USERSERVER_URL"]


@router.post(
    "",
    response_model=UserDB,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def create_user(
    payload: UserSchema,
    response: Response,
    x_access_token: Optional[str] = Header(None),
):
    auth_payload = {"email": payload.email}
    auth_header = {"x-access-token": x_access_token}
    registered_user, status_code = Requester.auth_srv_fetch(
        method="POST",
        path="/user/registered",
        payload=auth_payload,
        extra_headers=auth_header,
    )
    path = "/users"
    payload_user = payload.dict()
    payload_user.update({"id": registered_user["uuid"]})
    user, status_code = Requester.user_srv_fetch(
        method="POST", path=path, payload=payload_user
    )
    response.status_code = status_code
    return user


@router.get("/{user_id}", response_model=UserDB, status_code=HTTP_200_OK)
async def get_user(user_id: int, response: Response):
    path = f"/users/{user_id}"
    user, status_code = Requester.user_srv_fetch(method="GET", path=path)
    response.status_code = status_code
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
    response: Response,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't update info about other users")

    path = f"/users/{user_id}"
    new_user_info, status_code = Requester.user_srv_fetch(
        method="PATCH", path=path, payload=payload.dict(exclude_unset=True)
    )
    response.status_code = status_code
    return new_user_info


@router.delete(
    "/{user_id}", status_code=HTTP_200_OK, dependencies=[Depends(check_token)]
)
async def delete_user(
    user_id: int, response: Response, uuid: int = Depends(get_uuid_from_xtoken)
):
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't delete other users")

    path = f"/users/{user_id}"
    new_user_info, status_code = Requester.user_srv_fetch(method="DELETE", path=path)
    response.status_code = status_code
    return new_user_info


@router.get("", response_model=UserListSchema, status_code=HTTP_200_OK)
async def get_all_users(response: Response):
    path = "/users"
    users, status_code = Requester.user_srv_fetch(method="GET", path=path)
    response.status_code = status_code
    return users


@router.post(
    "/{user_id}/host_reviews",
    response_model=UserReviewSchema,
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_token)],
)
async def create_host_review(
    payload: UserReviewSchema,
    user_id: int,
    response: Response,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't create a review of other user")

    path = f"/users/{user_id}/host_reviews"
    review, status_code = Requester.user_srv_fetch(
        method="POST", path=path, payload=payload.dict()
    )

    response.status_code = status_code
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
    response: Response,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't create a rating of other user")

    path = f"/users/{user_id}/host_ratings"
    rating, status_code = Requester.user_srv_fetch(
        method="POST", path=path, payload=payload.dict()
    )

    response.status_code = status_code
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
    response: Response,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't create a review of other user")

    path = f"/users/{user_id}/guest_reviews"
    review, status_code = Requester.user_srv_fetch(
        method="POST", path=path, payload=payload.dict()
    )

    response.status_code = status_code
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
    response: Response,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't create a rating of other user")

    path = f"/users/{user_id}/guest_ratings"
    rating, status_code = Requester.user_srv_fetch(
        method="POST", path=path, payload=payload.dict()
    )

    response.status_code = status_code
    return rating


@router.get(
    "/{user_id}/host_reviews", response_model=UserReviewList, status_code=HTTP_200_OK
)
async def get_host_reviews(user_id: int, response: Response):
    path = f"/users/{user_id}/host_reviews"
    user_reviews, status_code = Requester.user_srv_fetch(method="GET", path=path)
    response.status_code = status_code
    return user_reviews


@router.get(
    "/{user_id}/host_ratings", response_model=UserRatingList, status_code=HTTP_200_OK
)
async def get_host_ratings(user_id: int, response: Response):
    path = f"/users/{user_id}/host_ratings"
    user_reviews, status_code = Requester.user_srv_fetch(method="GET", path=path)
    response.status_code = status_code
    return user_reviews


@router.get(
    "/{user_id}/guest_reviews", response_model=UserReviewList, status_code=HTTP_200_OK
)
async def get_guest_reviews(user_id: int, response: Response):
    path = f"/users/{user_id}/guest_reviews"
    user_reviews, status_code = Requester.user_srv_fetch(method="GET", path=path)
    response.status_code = status_code
    return user_reviews


@router.get(
    "/{user_id}/guest_ratings", response_model=UserRatingList, status_code=HTTP_200_OK
)
async def get_guest_ratings(user_id: int, response: Response):
    path = f"/users/{user_id}/guest_ratings"
    user_reviews, status_code = Requester.user_srv_fetch(method="GET", path=path)
    response.status_code = status_code
    return user_reviews


@router.get(
    "/{user_id}/host_reviews/{review_id}",
    response_model=UserReviewSchema,
    status_code=HTTP_200_OK,
)
async def get_single_host_review(user_id: int, review_id: int, response: Response):
    path = f"/users/{user_id}/host_reviews/{review_id}"
    user_reviews, status_code = Requester.user_srv_fetch(method="GET", path=path)
    response.status_code = status_code
    return user_reviews


@router.get(
    "/{user_id}/host_ratings/{rating_id}",
    response_model=UserRatingSchema,
    status_code=HTTP_200_OK,
)
async def get_single_host_rating(user_id: int, rating_id: int, response: Response):
    path = f"/users/{user_id}/host_ratings/{rating_id}"
    user_reviews, status_code = Requester.user_srv_fetch(method="GET", path=path)
    response.status_code = status_code
    return user_reviews


@router.get(
    "/{user_id}/guest_reviews/{review_id}",
    response_model=UserReviewSchema,
    status_code=HTTP_200_OK,
)
async def get_single_guest_review(user_id: int, review_id: int, response: Response):
    path = f"/users/{user_id}/guest_reviews/{review_id}"
    user_reviews, status_code = Requester.user_srv_fetch(method="GET", path=path)
    response.status_code = status_code
    return user_reviews


@router.get(
    "/{user_id}/guest_ratings/{rating_id}",
    response_model=UserRatingSchema,
    status_code=HTTP_200_OK,
)
async def get_single_guest_rating(user_id: int, rating_id: int, response: Response):
    path = f"/users/{user_id}/guest_ratings/{rating_id}"
    user_ratings, status_code = Requester.user_srv_fetch(method="GET", path=path)
    response.status_code = status_code
    return user_ratings


@router.patch(
    "/{user_id}/host_reviews/{review_id}",
    response_model=UserReviewSchema,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def update_host_review(
    user_id: int,
    review_id: int,
    payload: UserReviewUpdate,
    response: Response,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    review_path = f"/users/{user_id}/host_reviews/{review_id}"
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't edit a review of another user")

    review, status_code = Requester.user_srv_fetch(
        method="PATCH", path=review_path, payload=payload.dict(exclude_unset=True)
    )
    response.status_code = status_code
    return review


@router.patch(
    "/{user_id}/host_ratings/{rating_id}",
    response_model=UserRatingSchema,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def update_host_rating(
    user_id: int,
    rating_id: int,
    payload: UserRatingUpdate,
    response: Response,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    review_path = f"/users/{user_id}/host_ratings/{rating_id}"
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't edit a rating of another user")

    review, status_code = Requester.user_srv_fetch(
        method="PATCH", path=review_path, payload=payload.dict(exclude_unset=True)
    )
    response.status_code = status_code
    return review


@router.patch(
    "/{user_id}/guest_reviews/{review_id}",
    response_model=UserReviewSchema,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def update_guest_review(
    user_id: int,
    review_id: int,
    payload: UserReviewUpdate,
    response: Response,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    review_path = f"/users/{user_id}/guest_reviews/{review_id}"
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't edit a review of another user")

    review, status_code = Requester.user_srv_fetch(
        method="PATCH", path=review_path, payload=payload.dict(exclude_unset=True)
    )
    response.status_code = status_code
    return review


@router.patch(
    "/{user_id}/guest_ratings/{rating_id}",
    response_model=UserRatingSchema,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def update_guest_rating(
    user_id: int,
    rating_id: int,
    payload: UserRatingUpdate,
    response: Response,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    rating_path = f"/users/{user_id}/guest_ratings/{rating_id}"
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't edit a rating of another user")

    review, status_code = Requester.user_srv_fetch(
        method="PATCH", path=rating_path, payload=payload.dict(exclude_unset=True)
    )
    response.status_code = status_code
    return review


@router.delete(
    "/{user_id}/host_reviews/{review_id}",
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_host_review(
    user_id: int,
    review_id: int,
    response: Response,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    review_path = f"/users/{user_id}/host_reviews/{review_id}"
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't delete a review of another user")

    review, status_code = Requester.user_srv_fetch(method="DELETE", path=review_path)
    response.status_code = status_code
    return review


@router.delete(
    "/{user_id}/host_ratings/{rating_id}",
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_host_rating(
    user_id: int,
    rating_id: int,
    response: Response,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    rating_path = f"/users/{user_id}/host_ratings/{rating_id}"
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't delete a rating of another user")

    review, status_code = Requester.user_srv_fetch(method="DELETE", path=rating_path)
    response.status_code = status_code
    return review


@router.delete(
    "/{user_id}/guest_reviews/{review_id}",
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_guest_review(
    user_id: int,
    review_id: int,
    response: Response,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    review_path = f"/users/{user_id}/guest_reviews/{review_id}"
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't delete a review of another user")

    review, status_code = Requester.user_srv_fetch(method="DELETE", path=review_path)
    response.status_code = status_code
    return review


@router.delete(
    "/{user_id}/guest_ratings/{rating_id}",
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def delete_guest_rating(
    user_id: int,
    rating_id: int,
    response: Response,
    uuid: int = Depends(get_uuid_from_xtoken),
):
    rating_path = f"/users/{user_id}/guest_ratings/{rating_id}"
    if not AuthSender.has_permission_to_modify(uuid, user_id):
        raise UnauthorizedRequestError("You can't delete a rating of another user")

    review, status_code = Requester.user_srv_fetch(method="DELETE", path=rating_path)
    response.status_code = status_code
    return review
