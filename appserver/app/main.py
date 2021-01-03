import logging
import logging.config
import os

from app.api.routes import (booking_router, file_upload_router,
                            room_router, user_router)
from app.config import firebase_authenticate, get_settings
from app.db import Base, engine
from app.errors.auth_error import AuthException
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

logging_conf_path = os.path.join(os.path.dirname(__file__), "logging.ini")
logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)

Base.metadata.create_all(engine)
if get_settings().environment == "production":
    firebase_authenticate()

app = FastAPI(
    title="BookBNB Appserver", description="Especificacion sobre la API del appserver"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AuthException)
async def auth_exception_handler(_request, exc):
    error = {"error": exc.detail}
    return JSONResponse(status_code=exc.status_code, content=error)


@app.exception_handler(HTTPException)
async def http_exception_handler(_request, exc):
    error = {"error": exc.detail}
    return JSONResponse(status_code=exc.status_code, content=error)


app.include_router(booking_router.router, tags=["Bookings"])
app.include_router(file_upload_router.router, tags=["Images"])
app.include_router(room_router.router, prefix="/rooms", tags=["Rooms"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])

'''
@app.get(
    "/users/me",
    response_model=UserDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def get_current_user(uuid: int = Depends(get_uuid_from_xtoken)):
    path = f"/users/{uuid}"
    user, _ = Requester.user_srv_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return user


@app.get(
    "/users/me/wallet",
    response_model=WalletDB,
    status_code=HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def get_current_user_wallet(uuid: int = Depends(get_uuid_from_xtoken)):
    path = f"/wallets/{uuid}"
    wallet, _ = Requester.payment_fetch(
        method="GET", path=path, expected_statuses={HTTP_200_OK}
    )
    return wallet
'''