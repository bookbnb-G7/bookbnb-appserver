from fastapi import FastAPI

from app.api import ping
from app.api import notes

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
    return {"message":"pudiste crack!"}

@app.get("/facu")
async def facu():
	return {"message":"hola soy facu"}

@app.get("/nico")
async def nico():
	return {"message":"hola soy nico"}

app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
