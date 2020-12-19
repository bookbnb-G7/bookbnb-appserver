import logging
from typing import Optional

import app.errors.auth_error as ae
from app.services.authsender import AuthSender
from fastapi import Header

logger = logging.getLogger(__name__)


async def check_token(x_access_token: Optional[str] = Header(None)):
    if not x_access_token:
        logger.warning("No access token in header")
        raise ae.MissingTokenError()

    if not AuthSender.is_valid_token(x_access_token):
        logger.warning("Invalid access token")
        raise ae.InvalidIdTokenError()


async def get_uuid_from_xtoken(x_access_token: Optional[str] = Header(None)):
    return AuthSender.get_uuid_from_token(x_access_token)
