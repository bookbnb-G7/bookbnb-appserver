from fastapi import FastAPI
# from app.db import engine, metadata, database
from app.api.routes import room_router

app = FastAPI()


# """@app.on_event("startup")
# async def startup():
#     await database.connect()"""


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()"""


app.include_router(room_router.router, prefix="/rooms", tags=["rooms"])
