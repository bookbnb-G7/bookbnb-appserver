from fastapi import FastAPI
from app.api.routes import note_router
from app.db import engine, metadata, database

metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def pong():
    return {"message": "appserver"}


app.include_router(note_router.router, prefix="/notes", tags=["notes"])
