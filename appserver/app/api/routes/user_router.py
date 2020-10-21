from fastapi import APIRouter, HTTPException
from app.api.models.user_model import UserSchema

import requests as rq

router = APIRouter()

API_URL = 'https://bookbnb-userserver.herokuapp.com/users/'

@router.get('/{user_id}/')
async def read_user(user_id: int):
	user = rq.get(API_URL + str(user_id))
	return user.json()

@router.post('/')
async def create_post(payload: UserSchema):
	created_user = rq.post(API_URL, json=payload.dict())
	return created_user.json()