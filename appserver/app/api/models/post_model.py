from pydantic import BaseModel

class PostSchema(BaseModel):
    title: str
    body: str
    author: str