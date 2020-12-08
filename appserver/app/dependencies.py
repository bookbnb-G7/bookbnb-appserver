from typing import Optional

import app.errors.auth_error as ae
from app.services.authsender import AuthSender
from fastapi import Header


async def check_token(x_access_token: Optional[str] = Header(None)):
    if not x_access_token:
        raise ae.MissingTokenError()

    if not AuthSender.token_is_valid(x_access_token):
        raise ae.InvalidIdTokenError()


async def get_uuid_from_xtoken(x_access_token: Optional[str] = Header(None)):
    return AuthSender.get_uuid_from_token(x_access_token)
