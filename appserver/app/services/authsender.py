import logging
import os
from typing import Any, Dict, List

from app.errors.http_error import NotFoundError
from app.services.requester import Requester

logger = logging.getLogger(__name__)


class AuthSender:
    url = os.environ["AUTHSERVER_URL"]
    mock_db: List[Dict[str, Any]] = []

    @classmethod
    def tkn_hdr(cls, token):
        return {"x-access-token": token}

    @classmethod
    def is_valid_token(cls, token):
        response, code = Requester.auth_srv_fetch(
            method="POST",
            path="/auth/sign-in",
            payload={},
            extra_headers=cls.tkn_hdr(token),
        )
        logger.debug(
            "Auth server validate token response: %s, status_code: %s", response, code
        )

        return code == 200

    @classmethod
    def get_uuid_from_token(cls, token):
        # if not cls.url:
        #    cls._mock_get_info(int(token))
        #    return int(token)

        response, code = Requester.auth_srv_fetch(
            method="GET", path="/user/id", payload={}, extra_headers=cls.tkn_hdr(token)
        )
        logger.debug(
            "Auth server get uuid response: %s, status_code: %s", response, code
        )

        if code != 200:
            raise NotFoundError("User")

        logger.info("Obtained user uuid: %d", response["uuid"])
        return response["uuid"]

    @classmethod
    def has_permission_to_modify(cls, viewer_id, user_id):
        # an user can only modify its own things
        return (
            user_id == viewer_id
        )  # or cls.is_user_admin(viewer_id)[0].get("admin", False)

    @classmethod
    def has_permission_to_comment(cls, viewer_id, user_id):
        # an user can rate/review its own
        # rooms or himself (as host or guest)
        return (
            user_id != viewer_id
        )  # or cls.is_user_admin(viewer_id)[0].get("admin", False)

    @classmethod
    def can_book_room(cls, user_id, requester_id):
        return user_id != requester_id
