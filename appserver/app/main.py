from fastapi import FastAPI
from app.db import engine, metadata, database
from app.api.routes import post_router, note_router, user_router

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

app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(post_router.router, prefix="/posts", tags=["posts"])
app.include_router(note_router.router, prefix="/notes", tags=["notes"])