from fastapi import FastAPI
from app.db import Base, engine

# from app.db import engine, metadata, database
from app.api.routes import room_router, user_router, file_upload_router
from app.config import firebase_authenticate
from app.config import get_settings

Base.metadata.create_all(engine)

if get_settings().environment == "production":
    firebase_authenticate()
app = FastAPI(
    title="BookBNB Appserver", description="Especificacion sobre la API del appserver"
)

app.include_router(room_router.router, prefix="/rooms", tags=["Rooms"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(file_upload_router.router, tags=["Images"])
