from pydantic import BaseModel


class TokenSchema(BaseModel):
    push_token: str

