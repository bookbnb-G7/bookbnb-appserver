from app.api.crud import note_crud
from fastapi import APIRouter, HTTPException
from app.api.models.note_model import NoteDB, NoteSchema

router = APIRouter()

@router.post("/", response_model=NoteDB, status_code=201)
async def create_note(payload: NoteSchema):
    note_id = await note_crud.post(payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }

    return response_object

@router.get("/{note_id}/", response_model=NoteDB)
async def read_note(note_id: int):
    note = await note_crud.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
