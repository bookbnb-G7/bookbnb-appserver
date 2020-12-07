from fastapi import Header
from typing import Optional
import app.utils.token_utils as token_utils
from fastapi import APIRouter, Response
from app.services.requester import Requester
from app.services.authsender import AuthSender
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

#-----------------------------------ROOMS--------------------------------------#
@router.post("/", response_model=RoomDB, status_code=HTTP_201_CREATED)
async def create_room(payload: RoomSchema, response: Response,
    x_access_token: Optional[str] = Header(None)):
    
    token_utils.check_token(x_access_token)

    uuid = AuthSender.get_uuid_from_token(x_access_token)

    path = f'users/{uuid}'
    user = Requester.fetch_srv_users(method='GET', path=path)
    owner = f"{user['firstname']} {user['lastname']}"

    payload = payload.dict().add(owner_uuid=uuid, owner=owner)
    room, status_code = Requester.room_srv_fetch(method='POST', 
                                                 path='/rooms', 
                                                 payload=payload)
    response.status_code = status_code

    return room


@router.get("/", response_model=RoomList, status_code=HTTP_200_OK)
async def get_all_rooms(response: Response):
    token_utils.check_token(x_access_token)

    rooms, status_code = Requester.room_srv_fetch(method='GET', 
                                                  path='/rooms')
    response.status_code = status_code
    return rooms


@router.get("/{room_id}", response_model=RoomDB, status_code=HTTP_200_OK)
async def get_room(room_id: int, response: Response):
    token_utils.check_token(x_access_token)

    path = '/rooms' + f"/{room_id}"

    room, status_code = Requester.room_srv_fetch(method='GET', 
                                                 path=path)
    response.status_code = status_code
    return room


@router.patch("/{room_id}", response_model=RoomDB, status_code=HTTP_200_OK)
async def update_room(payload: RoomUpdate, room_id: int, response: Response):
    token_utils.check_token(x_access_token)

    path = '/rooms' + f"/{room_id}"
    viewer_uuid = AuthSender.get_uuid_from_token(token)
    room, status_code = Requester.room_srv_fetch(method='GET', path=path)        

    if not AuthSender.has_permission_to_modify(viewer_uuid, room['owner_uuid']):
        raise BadRequestError("You can't update other users rooms!")

    payload = payload.dict(exclude_unset=True)

    path = '/rooms' + f"/{room_id}"
    room, status_code = Requester.room_srv_fetch(method='PATCH', 
                                                 path=path, 
                                                 payload=payload)
    response.status_code = status_code
    return room


@router.delete("/{room_id}", response_model=RoomDB, status_code=HTTP_200_OK)
async def delete_room(room_id: int, response: Response):
    token_utils.check_token(x_access_token)

    path = '/rooms' + f"/{room_id}"
    viewer_uuid = AuthSender.get_uuid_from_token(token)
    room, status_code = Requester.room_srv_fetch(method='GET', path=path)   

    if not AuthSender.has_permission_to_modify(viewer_uuid, room['owner_uuid']):
        raise BadRequestError("You can't delete other users rooms!")

    path = '/rooms' + f"/{room_id}"
    room, status_code = Requester.room_srv_fetch(method='DELETE', 
                                                 path=path)
    response.status_code = room.status_code
    return room
#------------------------------------------------------------------------------#




#-----------------------------ROOMS-RATINGS------------------------------------#
@router.post("/{room_id}/ratings", response_model=RoomRatingDB, status_code=HTTP_201_CREATED)
async def rate_room(payload: RoomRatingSchema, room_id: int, response: Response):
    token_utils.check_token(x_access_token)

    path = '/rooms' + f"/{room_id}"
    viewer_uuid = AuthSender.get_uuid_from_token(token)
    room, status_code = Requester.room_srv_fetch(method='GET', path=path)

    if not AuthSender.has_permission_to_comment(viewer_uuid, room['owner_uuid']):
        raise BadRequestError("You can't rate your own rooms!")

    path = '/users' + f'/{viewer_uuid}'
    user, statis_code =Requester.user_srv_fetch(method='GET', path=path)
    reviewer_name = f"{user['firstname']} {user['lastname']}" 

    payload = payload.dict().add(reviewer_name=reviewer_name, 
                                 reviewer_uuid=viewer_uuid)

    path = '/rooms' + f"/{room_id}/ratings"
    rating, status_code = Requester.room_srv_fetch(method='POST', 
                                                   path=path, 
                                                   payload=payload)
    response.status_code = status_code
    return rating


@router.get("/{room_id}/ratings/{rating_id}",response_model=RoomRatingDB, status_code=HTTP_200_OK)
async def get_room_rating(room_id: int, rating_id: int, response: Response):
    token_utils.check_token(x_access_token)

    path = '/rooms' + f"/{room_id}/ratings/{rating_id}"
    rating, status_code = Requester.room_srv_fetch(method='GET', 
                                                   path=path)
    response.status_code = status_code
    return rating


@router.get("/{room_id}/ratings", response_model=RoomRatingList, status_code=HTTP_200_OK)
async def get_all_room_ratings(room_id: int, response: Response):
    token_utils.check_token(x_access_token)

    path = '/rooms' + f'/{room_id}/ratings'
    ratings, status_code = Requester.room_srv_fetch(method='GET', 
                                                   path=path)
    response.status_code = status_code
    return ratings


@router.patch("/{room_id}/ratings/{rating_id}", response_model=RoomRatingDB, status_code=HTTP_200_OK)
async def update_room_rating(payload: RoomRatingUpdate, 
    room_id: int, rating_id: int, response: Response):
    token_utils.check_token(x_access_token)
    
    path = f'/rooms/{room_id}/ratings/{rating_id}'
    viewer_uuid = AuthSender.get_uuid_from_token(token)
    rating, status_code = Requester.room_srv_fetch(method='GET', path=path)

    if not AuthSender.has_permission_to_modify(viewer_uuid, rating['reviewer_id']):
        raise BadRequestError("You can't update other users room ratings!")

    payload = payload.dict(exclude_unset=True)

    path = '/rooms' + f"/{room_id}/ratings/{rating_id}"
    rating, status_code = Requester.room_srv_fetch(method='PATCH',
                                                   path=path,
                                                   payload=payload)

    response.status_code = status_code
    return rating


@router.delete("/{room_id}/ratings/{rating_id}", response_model=RoomRatingDB, status_code=HTTP_200_OK)
async def delete_room_rating(room_id: int, rating_id: int, response: Response):
    token_utils.check_token(x_access_token)

    path = f"/{room_id}/ratings/{rating_id}"
    viewer_uuid = AuthSender.get_uuid_from_token(token)
    rating, status_code = Requester.room_srv_fetch(method='GET', path=path)   

    if not AuthSender.has_permission_to_modify(viewer_uuid, rating['reviewer_id']):
        raise BadRequestError("You can't delete other users room ratings!")

    path = f"/{room_id}/ratings/{rating_id}"
    rating, status_code = Requester.room_srv_fetch(method='DELETE', 
                                                   path=path)
    response.status_code = status_code
    return rating
#------------------------------------------------------------------------------#




#-----------------------------ROOMS-REVIEWS------------------------------------#
@router.post("/{room_id}/reviews", response_model=RoomReviewDB, status_code=HTTP_201_CREATED)
async def review_room(payload: RoomReviewSchema, room_id: int, response: Response):
    token_utils.check_token(x_access_token)

    path = '/rooms' + f"/{room_id}"
    viewer_uuid = AuthSender.get_uuid_from_token(token)
    room, status_code = Requester.room_srv_fetch(method='GET', path=path)

    if not AuthSender.has_permission_to_comment(viewer_uuid, room['owner_uuid']):
        raise BadRequestError("You can't review your own rooms!")

    path = '/users' + f'/{viewer_uuid}'
    user, statis_code = Requester.user_srv_fetch(method='GET', path=path)
    reviewer_name = f"{user['firstname']} {user['lastname']}" 

    payload = payload.dict().add(reviewer_name=reviewer_name, 
                                 reviewer_uuid=viewer_uuid)

    path = '/rooms' + f"/{room_id}/reviews"
    review, status_code = Requester.room_srv_fetch(method='POST', 
                                                   path=path, 
                                                   payload=payload)
    response.status_code = status_code
    return review


@router.get("/{room_id}/reviews/{review_id}", response_model=RoomReviewDB, status_code=HTTP_200_OK)
async def get_room_review(room_id: int, review_id: int, response: Response):
    token_utils.check_token(x_access_token)

    path = '/rooms' + f"/{room_id}/reviews/{review_id}"
    review, status_code = Requester.room_srv_fetch(method='GET', 
                                                   path=path)
    response.status_code = status_code
    return review


@router.get("/{room_id}/reviews", response_model=RoomReviewList, status_code=HTTP_200_OK)
async def get_all_room_reviews(room_id: int, response: Response):
    token_utils.check_token(x_access_token)

    path = '/rooms' + f'/{room_id}/reviews'
    reviews, status_code = Requester.room_srv_fetch(method='GET', 
                                                    path=path)
    response.status_code = status_code
    return reviews


@router.patch("/{room_id}/reviews/{review_id}", response_model=RoomReviewDB, status_code=HTTP_200_OK)
async def update_room_review(payload: RoomReviewUpdate, 
    room_id: int, review_id: int, response: Response):
    token_utils.check_token(x_access_token)

    path = f'/rooms/{room_id}/reviews/{review_id}'
    viewer_uuid = AuthSender.get_uuid_from_token(token)
    review, status_code = Requester.room_srv_fetch(method='GET', path=path)

    if not AuthSender.has_permission_to_modify(viewer_uuid, review['reviewer_id']):
        raise BadRequestError("You can't update other users room reviews!")

    payload = payload.dict(exclude_unset=True)
    path = '/rooms' + f"/{room_id}/ratings/{rating_id}"
    review, status_code = Requester.room_srv_fetch(method='PATCH',
                                                   path=path,
                                                   payload=payload)
    response.status_code = status_code
    return review


@router.delete("/{room_id}/reviews/{review_id}", response_model=RoomReviewDB, status_code=HTTP_200_OK)
async def delete_room_review(room_id: int, review_id: int, response: Response):
    token_utils.check_token(x_access_token)

    path = f"/{room_id}/reviews/{review_id}"
    viewer_uuid = AuthSender.get_uuid_from_token(token)
    review, status_code = Requester.room_srv_fetch(method='GET', path=path)   

    if not AuthSender.has_permission_to_modify(viewer_uuid, review['reviewer_id']):
        raise BadRequestError("You can't delete other users room reviews!")

    path = f"/{room_id}/reviews/{review_id}"
    review, status_code = Requester.room_srv_fetch(method='DELETE', 
                                                   path=path)
    response.status_code = status_code
    return review
#------------------------------------------------------------------------------#



