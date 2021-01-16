import os
import logging.config
from app.db import Base, engine
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse
from app.errors.auth_error import AuthException
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import booking_router, room_router, user_router, me_router

logging_conf_path = os.path.join(os.path.dirname(__file__), "logging.ini")
logging.config.fileConfig(logging_conf_path, disable_existing_loggers=False)

Base.metadata.create_all(engine)

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

app.include_router(me_router.router, prefix="/me", tags=["me"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(room_router.router, prefix="/rooms", tags=["Rooms"])
app.include_router(booking_router.router, prefix="/bookings", tags=["Bookings"])
