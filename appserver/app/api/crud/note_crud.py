from app.db import notes_table, database
from app.api.models.note_model import NoteSchema

async def post(payload: NoteSchema):
    query = notes_table.insert().values(title=payload.title, description=payload.description)
    return await database.execute(query=query)

async def get(note_id: int):
    query = notes_table.select().where(note_id == notes.c.id)
    return await database.fetch_one(query=query)
