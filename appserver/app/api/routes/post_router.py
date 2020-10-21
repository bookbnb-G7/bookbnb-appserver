from fastapi import APIRouter, HTTPException
from app.api.models.post_model import PostSchema

import requests as rq

router = APIRouter()

API_URL = 'https://bookbnb-postserver.herokuapp.com/posts/'

@router.get('/{post_id}/')
async def read_post(post_id: int):
	post = rq.get(API_URL + str(post_id))
	return post.json()

@router.post('/')
async def create_post(payload: PostSchema):
	created_post = rq.post(API_URL, json=payload.dict())
	return created_post.json()